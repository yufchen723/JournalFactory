"""Journal adaptation and the production line view for `jf`.

adapt   resolve a journal by name (or pick it from the evidence), or scaffold a profile for a
        journal that is not built in, then print how every stage is set up for it
figure  audit figure files against any journal profile
demo    six-panel demo figure (simulated data) in any journal's style
line    the nine stations for one project, with what exists at each
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent
JDIR = HOME / "journals"
DIMS = ["concept", "technology", "scale", "orthogonal", "replication", "function", "clinical", "resource"]

ALIASES = {
    "nc": "nature-communications", "ncomms": "nature-communications", "natcommun": "nature-communications", "natcomm": "nature-communications",
    "ng": "nature-genetics", "natgenet": "nature-genetics", "nbt": "nature-biotechnology", "natbiotechnol": "nature-biotechnology",
    "natbiotech": "nature-biotechnology", "nm": "nature-medicine", "natmed": "nature-medicine", "nmeth": "nature-methods",
    "natmethods": "nature-methods", "nn": "nature-neuroscience", "natneurosci": "nature-neuroscience", "natcancer": "nature-cancer",
    "crm": "cell-reports-medicine", "cellrepmed": "cell-reports-medicine", "cc": "cancer-cell", "neurooncol": "neuro-oncology",
}
FAMILY_TITLES = {
    "cell-press": ["cell", "immunity", "neuron", "molecular cell", "cancer cell", "cell reports", "cell stem cell", "cell metabolism",
                   "developmental cell", "cell systems", "cell genomics", "med", "cell host & microbe", "cell host and microbe", "current biology",
                   "structure", "iscience", "patterns", "cell chemical biology", "cell reports medicine", "cell reports methods", "trends"],
    "nature": ["nature", "communications biology", "communications medicine"],
    "science": ["science"],
}
FAMILY_TEMPLATE = {"cell-press": "cancer-cell", "nature": "nature-communications", "science": "science", "other": "neuro-oncology"}
FAMILY_PAGES = {
    "cell-press": "cell.com/<journal>/information-for-authors (article types, revise-manuscript, final-submission) and cell.com/information-for-authors/figure-guidelines",
    "nature": "nature.com/<journal>/submission-guidelines (formatting guide, article types) and the Nature Portfolio artwork guide",
    "science": "science.org/content/page/instructions-preparing-initial-manuscript and the journal's figure instructions",
    "other": "the journal's 'Instructions for authors' and artwork pages",
}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def journals() -> dict:
    return {p.stem: json.loads(p.read_text()) for p in sorted(JDIR.glob("*.json")) if not p.name.startswith("_")}


def resolve(name: str):
    """(id, how) for a built-in profile, or (None, suggestions)."""
    js = journals(); n = norm(name)
    if name in js:
        return name, "id"
    if n in ALIASES:
        return ALIASES[n], "abbreviation"
    for k, j in js.items():
        if n in (norm(k), norm(j["name"])):
            return k, "name"
    hits = [k for k, j in js.items() if n and (n in norm(j["name"]) or norm(j["name"]) in n)]
    exact_len = [k for k in hits if len(norm(js[k]["name"])) == len(n)]
    if len(exact_len) == 1:
        return exact_len[0], "name"
    return None, hits


def guess_family(name: str) -> str:
    low = name.lower().strip()
    for fam, titles in FAMILY_TITLES.items():
        if low in titles:
            return fam
    if low.startswith("nature ") or low.startswith("nat "):
        return "nature"
    if low.startswith("cell ") or low.startswith("trends in"):
        return "cell-press"
    if low.startswith("science "):
        return "science"
    return "other"


def scaffold(name: str, family: str | None, tier: int | None) -> tuple[str, dict]:
    """A draft profile for a journal that is not built in. Structure comes from the publisher
    family; every limit is left empty and the profile is marked `memory` until someone reads
    the journal's own pages. Nothing is invented."""
    fam = family or guess_family(name)
    tpl = json.loads((JDIR / f"{FAMILY_TEMPLATE[fam]}.json").read_text())
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    today = datetime.date.today().isoformat()
    p = {
        "id": slug, "name": name, "publisher": tpl.get("publisher") if fam != "other" else None, "family": fam,
        "article_type": tpl.get("article_type"), "tier": tier or 3,
        "scope": "not written yet: read the journal's aims and scope, and five recent papers close to yours",
        "limits": {k: None for k in tpl["limits"]},
        "figure": {**{k: v for k, v in tpl["figure"].items() if k not in ("notes", "max_height_note", "gray_fill", "graphical_abstract", "max_file_mb", "recommended_max_mm")},
                   "notes": [f"Copied from the {fam} family template ({tpl['name']}). Confirm every number on the journal's artwork page."]},
        "sections": tpl["sections"], "front_matter": tpl["front_matter"], "methods": {**tpl["methods"], "word_limit": None},
        "supplemental": tpl["supplemental"], "citation_style": tpl.get("citation_style"), "extras": tpl.get("extras", []),
        "bar": dict(tpl["bar"]),
        "verified": {"level": "memory", "date": today, "scaffold": True,
                     "note": f"Scaffold from the {fam} family template. Limits are empty and figure rules are the family's usual ones; nothing was read on the journal's site."},
        "sources": [{"url": FAMILY_PAGES[fam], "status": "not-read", "date": today}],
        "skills": tpl.get("skills", []),
        "to_confirm": ["article types and word limits", "number of main display items", "abstract / summary length", "title length", "reference limit and style",
                       "figure widths, type sizes, panel letters, file formats, resolution", "extra-figure naming and limits", "methods section name and limit",
                       "front matter (highlights, blurbs, graphical abstract)", "data, code and reporting requirements", "AI policy for text and images",
                       "evidence bar (jf fit): score five recent comparable papers on the eight dimensions"],
    }
    return slug, p


def pick_from_evidence(paper_path: str, scenario: str | None):
    paper = json.loads(Path(paper_path).read_text())
    scen = paper.get("scenarios", {"current": paper.get("scores", {})})
    name = scenario or next(iter(scen))
    s = scen[name]["scores"] if isinstance(scen[name], dict) and "scores" in scen[name] else scen[name]
    rows = []
    for k, j in journals().items():
        gap = sum(max(0, j["bar"][d] - s.get(d, 0)) for d in DIMS)
        rows.append((gap > 0, j["tier"], gap, k))
    rows.sort()
    fits = [r for r in rows if not r[0]]
    return name, (fits[0][3] if fits else None), rows


def _fmt_limits(L: dict) -> list[str]:
    lab = {"main_display_items": "main display items", "main_text_words": "main text (words)", "abstract_words": "abstract / summary (words)",
           "title_chars": "title (characters)", "references": "references", "methods_words": "methods (words)", "legend_words": "legend (words)",
           "extended_items": "extended data items", "keywords": "keywords", "etoc_words": "eTOC blurb (words)", "etoc_sentences": "eTOC sentences",
           "supplemental_figures_recommended": "supplemental figures (recommended max)"}
    out = []
    for k, v in L.items():
        if k == "highlights" and v:
            out.append(f"highlights: {v['n']} bullets, {v['chars']} characters each")
        elif isinstance(v, (int, float)):
            out.append(f"{lab.get(k, k)}: {v:g}")
        elif v is None and k in lab:
            out.append(f"{lab[k]}: not stated in the profile")
    return out


def sheet(j: dict) -> str:
    F = j["figure"]; v = j["verified"]; jid = j["id"]
    W = ", ".join(f"{k} {val:g}" for k, val in F["widths_mm"].items())
    case = "A, B, C" if F["panel_label"].get("case") == "upper" else "a, b, c"
    own_cell = jid == "cell"
    pack = ("cell-skills/ (figure, writing, statistics, reviewer, response, data, citation)" if own_cell else
            "cell-skills/ for Cell Press structure, then " + ", ".join(s for s in j.get("skills", []) if "cell-skills (" not in s) if j.get("family") == "cell-press" else
            ", ".join(j.get("skills", [])) or "vendor/k-dense/venue-templates, vendor/k-dense/scientific-writing")
    L = [f"# Production line set for {j['name']}", "",
         f"Profile: journals/{jid}.json — verified: {v['level']}" + (f" ({v.get('date')})" if v.get("date") else "") + f". {v.get('note', '')}".rstrip()]
    if v["level"] != "official":
        L.append("=> These numbers were NOT read on the journal's own pages. Use them to plan and draft; confirm before formatting final files.")
    if j.get("to_confirm"):
        L += ["", "To confirm on the journal's site (" + j["sources"][0]["url"] + "):"] + [f"  [ ] {x}" for x in j["to_confirm"]]
    L += ["", "## 2 Journal fit", "  evidence bar (0-3): " + ", ".join(f"{d} {j['bar'][d]}" for d in DIMS) + (" (placeholder copied from the template)" if v.get("scaffold") else ""), f"  jf fit projects/<p>/paper.json   (tier {j['tier']})",
          "", "## 3 Story and structure"] + [f"  {x}" for x in _fmt_limits(j["limits"])[:1]] + [f"  extra figures: {j['supplemental']['figures']}"]
    L += ["", "## 4 Figures", f"  widths (mm): {W}; maximum height {F.get('max_height_mm', '?')} mm",
          f"  type: {' or '.join(F['font_family'])}, {F['font_pt']['min']:g}-{F['font_pt']['max']:g} pt; panel letters {case}, {F['panel_label'].get('pt', '?')} pt" + (" bold" if F["panel_label"].get("bold") else ""),
          f"  strokes: {F['line_pt']['min']:g}-{F['line_pt']['max']:g} pt; resolution: " + ", ".join(f"{k.replace('_', ' ')} {val}" for k, val in F["dpi"].items()) + " dpi",
          f"  files: {', '.join(F['formats'])}" + (f"; up to {F['max_file_mb']} MB each" if F.get("max_file_mb") else ""),
          f"  draw:   import journal_style as js; js.use_journal(\"{jid}\"); js.mosaic(...); js.label_panels(axd); js.save(fig, \"Figure 1\")",
          f"  check:  jf figure \"Figure 1.pdf\" --journal {jid}        demo: jf demo out/ --journal {jid}"]
    L += ["", "## 5 Text"] + [f"  {x}" for x in _fmt_limits(j["limits"])] + [f"  order: {' · '.join(j['sections'])}", f"  front matter: {'; '.join(j['front_matter'])}",
          f"  check:  jf count manuscript.md --journal {jid}" + ("        and: jf cell text manuscript.md" if own_cell else "")]
    L += ["", "## 6 Statistics and methods", f"  methods section: {j['methods']['name']}" + (f" (<= {j['methods']['word_limit']} words)" if j["methods"].get("word_limit") else ""),
          "  check:  jf cell legends legends.md   (what a legend must state; journal-neutral)" if not own_cell else "  check:  jf cell legends legends.md",
          "", "## 7 Submission", "  also required: " + ("; ".join(j.get("extras", [])) or "see the journal's checklist"),
          "", "## 8 Revision", "  check:  jf cell response response.md   (every comment answered, changes located; journal-neutral)",
          "", "## Studio", f"  jf paper init <dir> --journal {jid} --title \"...\" --figures {j['limits'].get('main_display_items') or 6}", "  jf studio --studio <dir>/.studio start",
          "", "## Skill pack to open", f"  {pack}"]
    return "\n".join(L)


def cmd_adapt(a):
    name = " ".join(a.journal)
    if norm(name) == "auto":
        if not a.paper:
            raise SystemExit("jf adapt auto needs --paper projects/<p>/paper.json (the evidence scores)")
        scen, jid, rows = pick_from_evidence(a.paper, a.scenario)
        print(f"Scenario '{scen}': journals ordered by fit, then tier")
        for short, tier, gap, k in rows[:6]:
            print(f"  {'fits ' if not short else 'short by ' + str(gap):12} tier {tier}  {k}")
        if not jid:
            raise SystemExit("\nNo journal fits this scenario yet. See `jf fit` for what is short, or name the journal: jf adapt <journal>")
        print(f"\nHighest-tier journal that fits: {jid}\n")
    else:
        jid, how = resolve(name)
        if jid is None:
            if not a.new:
                sug = f" Close matches: {', '.join(how)}." if how else ""
                raise SystemExit(f"'{name}' is not a built-in journal.{sug}\nBuilt in: {', '.join(journals())}\n"
                                 f"To set the line up for it anyway: jf adapt \"{name}\" --new [--family cell-press|nature|science|other] [--tier 1-4]")
            slug, p = scaffold(name, a.family, a.tier)
            f = JDIR / f"{slug}.json"
            if f.exists():
                raise SystemExit(f"{f} already exists")
            f.write_text(json.dumps(p, indent=1, ensure_ascii=False) + "\n")
            print(f"Created journals/{slug}.json from the {p['family']} family template (verified: memory).\n")
            jid = slug
    j = journals()[jid]
    if a.json:
        print(json.dumps(j, indent=1, ensure_ascii=False)); return
    print(sheet(j))
    if a.set:
        pp = Path(a.set); d = json.loads(pp.read_text()); old = d.get("target"); d["target"] = jid
        pp.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
        print(f"\nTarget in {pp}: {old} -> {jid}")


def _kit(args):
    return subprocess.call([sys.executable, str(HOME / "scripts" / "journal_style.py")] + args)


def cmd_figure(a):
    jid, _ = resolve(a.journal)
    if jid is None:
        raise SystemExit(f"unknown journal '{a.journal}'")
    extra = ["--kind", a.kind, "--stage", a.stage] + (["--width-mm", str(a.width_mm)] if a.width_mm else [])
    return _kit([jid, "--check"] + a.files + extra)


def cmd_demo(a):
    jid, _ = resolve(a.journal)
    if jid is None:
        raise SystemExit(f"unknown journal '{a.journal}'")
    return _kit([jid, "--demo", a.outdir])


def _words(t: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][\w'’\-/.%]*", re.sub(r"<[^>]+>|[*_`#>|]", " ", t)))


def cmd_line(a):
    pp = Path(a.paper); paper = json.loads(pp.read_text()); js = journals()
    jid = paper.get("target") or paper.get("journal"); j = js.get(jid)
    rows = []
    scen = paper.get("scenarios") or ({"current": paper["scores"]} if paper.get("scores") else {})
    rows.append(("0 Inventory", "done" if scen else "to do", f"{len(scen)} scenario(s) scored" if scen else "score the eight dimensions in paper.json"))
    slug = paper.get("field"); fd = HOME / "fields" / str(slug) if slug else None
    if fd and fd.is_dir():
        n = sum(1 for _ in open(fd / "papers.jsonl")) if (fd / "papers.jsonl").is_file() else 0
        st = "done" if (fd / "field_map.md").is_file() and n else "in progress"
        rows.append(("1 Field", st, f"{n} paper cards; field map {'written' if (fd / 'field_map.md').is_file() else 'not written'} (fields/{slug}/)"))
    else:
        rows.append(("1 Field", "to do", "jf field init <slug> --title \"...\""))
    if j and scen:
        first = next(iter(scen)); s = scen[first]["scores"] if isinstance(scen[first], dict) and "scores" in scen[first] else scen[first]
        gap = {d: j["bar"][d] - s.get(d, 0) for d in DIMS if j["bar"][d] > s.get(d, 0)}
        tot = sum(gap.values()); verdict = "fits" if not tot else "reach" if tot <= 2 else "not yet"
        rows.append(("2 Journal", "done", f"target {j['name']} ({j['verified']['level']} profile); scenario '{first}': {verdict}" + (" — short on " + ", ".join(f"{d} +{g}" for d, g in gap.items()) if gap else "")))
    else:
        rows.append(("2 Journal", "to do" if not j else "in progress", f"target {j['name']}; no scores to compare" if j else "jf adapt auto --paper <paper.json>, or jf adapt <journal>"))
    pr = paper.get("plan_report"); prp = (pp.parent / pr) if pr else None
    rows.append(("3 Story", "done" if prp and prp.exists() else "to do", f"plan: {pr}" if prp and prp.exists() else "plan report with every panel marked have / draw / needs analysis / needs new data"))
    ws = Path(a.workspace) if a.workspace else (pp.parent / paper["workspace"] if paper.get("workspace") else None)
    if ws and ws.is_dir():
        figs = sorted((ws / "figures").glob("fig[0-9]*/folio.json")) if (ws / "figures").is_dir() else []
        withp = 0
        for f in figs:
            try:
                withp += any(b.get("type") == "image" for b in json.loads(f.read_text()).get("blocks", []))
            except Exception:
                pass
        want = (j or {}).get("limits", {}).get("main_display_items")
        st = "to do" if not withp else "done" if figs and withp == len(figs) else "in progress"
        rows.append(("4 Figures", st, f"{withp} of {len(figs)} main figure pages have panels" + (f" (journal allows {want})" if want else "")))
        mt = ws / "text" / "main" / "folio.json"; n = 0
        if mt.is_file():
            for b in json.loads(mt.read_text()).get("blocks", []):
                if b.get("type") == "text":
                    t = b.get("text") or ""
                    if not t and b.get("file") and (mt.parent / b["file"]).is_file():
                        t = (mt.parent / b["file"]).read_text()
                    n += _words(t)
        lim = (j or {}).get("limits", {}).get("main_text_words")
        rows.append(("5 Text", "to do" if n < 200 else "in progress", f"{n} words in the main-text page" + (f" (limit about {lim}, counted by jf count)" if lim else "")))
    else:
        rows.append(("4 Figures", "to do", "jf paper init <dir> --journal <id> --title \"...\"  (then pass --workspace <dir>)"))
        rows.append(("5 Text", "to do", "written in the studio's main-text page"))
    for n, key, hint in (("6 Statistics", "statistics", "replicate unit and test per panel; jf cell legends"), ("7 Submission", "submission", "cover letter, front matter, deposits, final files"),
                         ("8 Revision", "revision", "after the decision letter: jf cell response")):
        d = paper.get("stages", {}).get(key)
        rows.append((n, d.get("status", "in progress") if isinstance(d, dict) else "to do", (d.get("note") if isinstance(d, dict) else None) or hint))
    mark = {"done": "[x]", "in progress": "[~]", "to do": "[ ]"}
    print(f"{paper.get('title', pp.name)}\n")
    for n, st, note in rows:
        print(f"  {mark.get(st, '[ ]')} {n:14}{st:12} {note}")
    nxt = next((r for r in rows if r[1] != "done"), None)
    print(f"\nNext station: {nxt[0]} — {nxt[2]}" if nxt else "\nAll stations done.")
    print("Stations 6-8 are marked by hand in paper.json: \"stages\": {\"statistics\": {\"status\": \"done\", \"note\": \"...\"}}")


def register(sp):
    p = sp.add_parser("adapt", help="set the whole line up for a journal (by name, by evidence, or a new one)")
    p.add_argument("journal", nargs="+", help='journal id or name, e.g. nature, "Cancer Cell", nc; or "auto" with --paper')
    p.add_argument("--paper", help="project paper.json (for auto)"); p.add_argument("--scenario")
    p.add_argument("--new", action="store_true", help="create a draft profile for a journal that is not built in")
    p.add_argument("--family", choices=list(FAMILY_TEMPLATE)); p.add_argument("--tier", type=int)
    p.add_argument("--set", metavar="PAPER_JSON", help="also write the journal as the project's target"); p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_adapt)
    p = sp.add_parser("figure", help="audit figure files against a journal profile")
    p.add_argument("files", nargs="+"); p.add_argument("--journal", required=True); p.add_argument("--kind", default="colour")
    p.add_argument("--stage", default="production", choices=("production", "initial")); p.add_argument("--width-mm", type=float); p.set_defaults(f=cmd_figure)
    p = sp.add_parser("demo", help="demo figure (simulated data) in a journal's style")
    p.add_argument("outdir"); p.add_argument("--journal", required=True); p.set_defaults(f=cmd_demo)
    p = sp.add_parser("line", help="the nine stations for one project")
    p.add_argument("paper"); p.add_argument("--workspace"); p.set_defaults(f=cmd_line)
