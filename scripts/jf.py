#!/usr/bin/env python3
"""jf — Journal Factory command line (stdlib only; PIL, pdfinfo, pdffonts, pdftotext used when present).

  jf journals                              list journal profiles (limits, figure widths, how each number was verified)
  jf journal <id>                          one profile in full
  jf compare <id> <id> ...                 side-by-side table (Markdown)
  jf fit <paper.json> [--scenario NAME]    compare a paper's evidence scores with each journal's bar
  jf count <text.md> --journal <id>        words per section against the journal's limits
  jf check-figure <file> --journal <id> [--width single|mid|double]
                                           page size, fonts, text size, resolution against the journal's figure rules
  jf field init <slug> --title "..."       start a field scan folder
  jf field scan <slug> [--max 40]          run fields/<slug>/queries.tsv on PubMed -> candidates.tsv
  jf field merge <slug>                    raw/*.jsonl -> papers.jsonl (deduplicated) + counts
  jf field verify <slug>                   check every PMID / title / year on PubMed
  jf field html <slug>                     browsable field map (timeline + filterable table)
  jf paper init <dir> --journal <id> --title "..." [--figures 7] [--supp 7]
                                           manuscript workspace in the built-in studio (main text, figures, front matter)
  jf studio <command ...>                  the built-in writing + figure studio (start, ls, show, set, check, shot, export, pending, answer ...)
  jf cartoon search|get|fetch|sync ...     BioCartoon icons (built in; local catalogue)
  jf doctor                                what is installed, what is missing

Nothing here writes outside the Journal Factory folder or the directory you name.
"""
import argparse, glob, html, json, os, re, shutil, subprocess, sys
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent
JDIR = HOME / "journals"
DIMS = ["concept", "technology", "scale", "orthogonal", "replication", "function", "clinical", "resource"]


def journals():
    return {p.stem: json.loads(p.read_text()) for p in sorted(JDIR.glob("*.json")) if not p.name.startswith("_")}


def J(jid):
    js = journals()
    if jid not in js:
        raise SystemExit(f"unknown journal '{jid}'. Known: {', '.join(js)}")
    return js[jid]


def widths(j):
    return ", ".join(f"{k} {v}" for k, v in j["figure"]["widths_mm"].items())


def cmd_journals(a):
    print(f"{'id':24}{'tier':5}{'figs':5}{'words':7}{'abstract':9}{'widths (mm)':34}verified")
    for k, j in journals().items():
        L = j["limits"]
        print(f"{k:24}{j['tier']:<5}{str(L.get('main_display_items') or '-'):5}{str(L.get('main_text_words') or '-'):7}{str(L.get('abstract_words') or '-'):9}{widths(j):34}{j['verified']['level']}")
    print("\nverified: official = read on the journal site; secondary = other sources that agree; memory = confirm before use.")


def cmd_journal(a):
    print(json.dumps(J(a.id), indent=1, ensure_ascii=False))


def cmd_compare(a):
    js = [J(i) for i in a.ids]
    rows = [("Main display items", lambda j: j["limits"].get("main_display_items")), ("Main text (words)", lambda j: j["limits"].get("main_text_words")),
            ("Abstract (words)", lambda j: j["limits"].get("abstract_words")), ("References", lambda j: j["limits"].get("references")),
            ("Methods", lambda j: j["methods"]["name"] + (f" (<= {j['methods']['word_limit']} words)" if j["methods"].get("word_limit") else "")),
            ("Extra figures", lambda j: j["supplemental"]["figures"]), ("Figure widths (mm)", widths),
            ("Text size (pt)", lambda j: f"{j['figure']['font_pt']['min']}-{j['figure']['font_pt']['max']}"),
            ("Panel letters", lambda j: ("A, B, C" if j["figure"]["panel_label"]["case"] == "upper" else "a, b, c") + f" {j['figure']['panel_label']['pt']} pt bold"),
            ("Front matter", lambda j: "; ".join(j["front_matter"])), ("Verified", lambda j: j["verified"]["level"])]
    print("| | " + " | ".join(j["name"] for j in js) + " |\n|---|" + "---|" * len(js))
    for name, f in rows:
        print(f"| {name} | " + " | ".join(str(f(j) if f(j) is not None else "not stated") for j in js) + " |")


def cmd_fit(a):
    paper = json.loads(Path(a.paper).read_text())
    scen = paper.get("scenarios", {"current": paper.get("scores", {})})
    names = [a.scenario] if a.scenario else list(scen)
    js = journals()
    for name in names:
        s = scen[name]["scores"] if "scores" in scen[name] else scen[name]
        print(f"\n## Scenario: {name}" + (f" — {scen[name].get('adds', '')}" if isinstance(scen[name], dict) and scen[name].get("adds") else ""))
        print("scores: " + ", ".join(f"{d} {s.get(d, 0)}" for d in DIMS))
        out = []
        for k, j in js.items():
            gaps = {d: j["bar"][d] - s.get(d, 0) for d in DIMS if j["bar"][d] > s.get(d, 0)}
            tot = sum(gaps.values())
            verdict = "fits" if tot == 0 else "reach" if tot <= 2 else "not yet"
            out.append((tot, j["tier"], k, verdict, gaps))
        for tot, tier, k, verdict, gaps in sorted(out):
            print(f"  {verdict:8} {k:24} tier {tier}  " + ("" if not gaps else "short on: " + ", ".join(f"{d} (+{g})" for d, g in gaps.items())))
    print("\nBars are a reading of recently published comparators (journals/_dimensions.json), not journal policy.")


SEC_ALIASES = {"summary": "abstract", "abstract": "abstract", "in brief": "etoc", "etoc": "etoc", "etoc blurb": "etoc", "highlights": "highlights", "title": "title",
               "star methods": "methods", "methods": "methods", "materials and methods": "methods", "online methods": "methods", "references": "references",
               "figure legends": "legends", "supplemental information": "supp", "key resources table": "methods", "acknowledgments": "back", "acknowledgements": "back",
               "author contributions": "back", "declaration of interests": "back", "competing interests": "back", "data availability": "back", "code availability": "back",
               "resource availability": "back", "keywords": "back"}


def cmd_count(a):
    j = J(a.journal); L = j["limits"]
    txt = Path(a.file).read_text()
    secs, cur = {}, "front"
    order = []
    for line in txt.splitlines():
        m = re.match(r"^#{1,2}\s+(.*)", line)
        if m:
            cur = m.group(1).strip()
            if cur not in secs:
                order.append(cur)
            secs.setdefault(cur, [])
            continue
        secs.setdefault(cur, []).append(line)
    words = lambda t: len(re.findall(r"[A-Za-z0-9][\w'’\-/.%]*", re.sub(r"<[^>]+>|\[\^?\d+\]|[*_`#>|]", " ", t)))
    main = 0; rows = []
    for name in order:
        body = "\n".join(secs[name]); kind = SEC_ALIASES.get(re.sub(r"[^a-z ]", "", name.lower()).strip(), "main")
        n = words(body); limit = ""; flag = ""
        if kind == "abstract" and L.get("abstract_words"):
            limit = L["abstract_words"]; flag = "OVER" if n > limit else "ok"
        elif kind == "etoc" and L.get("etoc_words"):
            limit = L["etoc_words"]; flag = "OVER" if n > limit else "ok"
        elif kind == "highlights" and L.get("highlights"):
            bl = [re.sub(r"^\s*[-*•]\s*", "", x).strip() for x in secs[name] if re.match(r"^\s*[-*•]", x)]
            over = [len(b) for b in bl if len(b) > L["highlights"]["chars"]]
            limit = f"{L['highlights']['n']} x {L['highlights']['chars']} chars"; flag = "OVER" if over or len(bl) > L["highlights"]["n"] else "ok"
            n = f"{len(bl)} bullets, longest {max([len(b) for b in bl] or [0])} chars"
        elif kind == "methods" and j["methods"].get("word_limit"):
            limit = j["methods"]["word_limit"]; flag = "OVER" if n > limit else "ok"
        elif kind in ("main", "legends") and name != "front":
            main += n
        rows.append((name, kind, n, limit, flag))
    print(f"{j['name']}: {a.file}\n{'section':44}{'kind':10}{'count':>26}  {'limit':>18}  ")
    for r in rows:
        print(f"{r[0][:43]:44}{r[1]:10}{str(r[2]):>26}  {str(r[3]):>18}  {r[4]}")
    lim = L.get("main_text_words")
    print(f"\nmain text (Introduction to Discussion + figure legends): {main} words" + (f"; limit about {lim}: {'OVER by ' + str(main - lim) if main > lim else 'ok'}" if lim else ""))
    refs = len(re.findall(r"(?m)^\s*\d+\.\s", "\n".join(secs.get("References", []))))
    if L.get("references") and refs:
        print(f"references: {refs}; limit about {L['references']}: {'OVER' if refs > L['references'] else 'ok'}")
    print(f"limits verified: {j['verified']['level']} — {j['verified']['note']}")


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def cmd_check_figure(a):
    j = J(a.journal); F = j["figure"]; f = a.file; ext = f.lower().rsplit(".", 1)[-1]
    issues, info = [], []
    w_mm = h_mm = None; sizes = []; fonts = set()
    if ext == "pdf":
        m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", run(["pdfinfo", f]))
        if m:
            w_mm, h_mm = float(m.group(1)) / 72 * 25.4, float(m.group(2)) / 72 * 25.4
        for line in run(["pdffonts", f]).splitlines()[2:]:
            p = line.split()
            if p:
                fonts.add(re.sub(r"^[A-Z]{6}\+", "", p[0]))
                if "Type 3" in line:
                    issues.append(f"Type 3 font {p[0]}: text is not editable (matplotlib: set pdf.fonttype 42)")
                if re.search(r"\sno\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line):
                    issues.append(f"font {p[0]} is not embedded")
        bb = run(["pdftotext", "-bbox", f, "-"])
        sizes = [float(y2) - float(y1) for y1, y2 in re.findall(r'<word xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)"', bb)]
        info.append("text size is estimated from word-box height (pdftotext); allow about 10%")
        if not sizes:
            issues.append("no selectable text found: text may be outlined or the figure is a raster image")
    elif ext == "svg":
        s = Path(f).read_text(errors="replace")
        unit = {"mm": 1, "cm": 10, "in": 25.4, "pt": 25.4 / 72, "px": 25.4 / 96, "": 25.4 / 96}
        m = re.search(r'<svg[^>]*?\swidth="([\d.]+)(mm|cm|in|pt|px)?"[^>]*?\sheight="([\d.]+)(mm|cm|in|pt|px)?"', s, re.S) or None
        if m:
            w_mm, h_mm = float(m.group(1)) * unit[m.group(2) or ""], float(m.group(3)) * unit[m.group(4) or ""]
        vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', s)
        scale = (w_mm / 25.4 * 72) / float(vb.group(1)) if (vb and w_mm) else 1.0
        for v, u in re.findall(r"font-size\s*[:=]\s*[\"']?([\d.]+)(px|pt|mm)?", s):
            sizes.append(float(v) * (0.75 if u in ("px", "") else 72 / 25.4 if u == "mm" else 1) * (scale if u in ("px", "") and vb else 1))
        fonts = {x.strip(" '\"").split(",")[0].strip(" '\"") for x in re.findall(r"font-family\s*[:=]\s*[\"']?([^;\"'>]+)", s)}
        if "<text" not in s and "<path" in s:
            issues.append("no <text> elements: text is outlined (matplotlib: set svg.fonttype none)")
    else:
        try:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            im = Image.open(f); dpi = im.info.get("dpi", (None, None))[0]
            target = F["widths_mm"].get(a.width or "double") or max(F["widths_mm"].values())
            eff = im.width / (target / 25.4)
            info.append(f"{im.width} x {im.height} px; stored dpi {dpi}; at {target} mm wide this is {eff:.0f} dpi")
            need = F["dpi"].get("photo", 300)
            if eff < need:
                issues.append(f"resolution {eff:.0f} dpi at {target} mm is below {need} dpi")
            issues.append("raster file: text inside cannot be edited or checked; export vector (PDF/SVG) for line art and labels")
            w_mm, h_mm = target, target * im.height / im.width
        except Exception as e:
            raise SystemExit(f"cannot read {f}: {e}")
    if w_mm:
        allowed = F["widths_mm"]; near = min(allowed.items(), key=lambda kv: abs(kv[1] - w_mm))
        info.append(f"page {w_mm:.1f} x {h_mm:.1f} mm; nearest allowed width: {near[0]} {near[1]} mm")
        if abs(near[1] - w_mm) > 1.5:
            issues.append(f"width {w_mm:.1f} mm is not one of {widths(j)}")
        if h_mm > F["max_height_mm"] + 0.5:
            issues.append(f"height {h_mm:.1f} mm exceeds {F['max_height_mm']} mm")
    if sizes:
        lo, hi = min(sizes), max(sizes); info.append(f"text size {lo:.1f}-{hi:.1f} pt in {len(sizes)} runs")
        if lo < F["font_pt"]["min"] - 0.6:
            issues.append(f"smallest text {lo:.1f} pt is below {F['font_pt']['min']} pt ({sum(s < F['font_pt']['min'] - 0.6 for s in sizes)} runs)")
        if hi > max(F["font_pt"]["max"], F["panel_label"]["pt"]) + 1.5:
            info.append(f"largest text {hi:.1f} pt is above the {F['font_pt']['max']} pt body range (fine for panel letters or titles in a draft)")
    if fonts:
        ok = [x.lower() for x in F["font_family"]] + ["arialmt", "helvetica", "liberationsans", "dejavusans" if False else "arial"]
        bad = sorted(x for x in fonts if x and not any(o.replace(" ", "") in x.lower().replace(" ", "").replace("-", "") for o in ok))
        info.append("fonts: " + ", ".join(sorted(fonts)))
        if bad:
            issues.append(f"fonts outside {', '.join(F['font_family'])}: {', '.join(bad)}")
    print(f"{j['name']} figure check: {f}")
    for i in info:
        print("  ·", i)
    for i in issues:
        print("  ✗", i)
    print("  ✓ no problems found" if not issues else f"  {len(issues)} problem(s)")
    print(f"  rules: {widths(j)} mm wide; text {F['font_pt']['min']}-{F['font_pt']['max']} pt {'/'.join(F['font_family'])}; panel letters "
          f"{'A B C' if F['panel_label']['case'] == 'upper' else 'a b c'}; verified: {j['verified']['level']}")
    return 1 if issues else 0


# ----------------------------------------------------------------------------- field scans
def fdir(slug):
    return HOME / "fields" / slug


def load_jsonl(p):
    out = []
    for line in open(p):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                print("  bad JSON line skipped in", p, file=sys.stderr)
    return out


def cmd_field(a):
    d = fdir(a.slug)
    if a.sub == "init":
        (d / "raw").mkdir(parents=True, exist_ok=True)
        if not (d / "queries.tsv").exists():
            shutil.copy(HOME / "templates" / "field_queries.tsv", d / "queries.tsv")
        if not (d / "field.json").exists():
            json.dump({"slug": a.slug, "title": a.title or a.slug, "question": "", "scope": {"years": [2014, 2026], "include": [], "exclude": []}, "scans": []}, open(d / "field.json", "w"), indent=1)
        print("created", d, "\nnext: edit queries.tsv, then: jf field scan", a.slug)
    elif a.sub == "scan":
        sys.path.insert(0, str(HOME / "scripts")); import pubmed
        have = {str(p.get("pmid")) for p in load_jsonl(d / "papers.jsonl")} if (d / "papers.jsonl").exists() else set()
        hits = {}
        for line in open(d / "queries.tsv"):
            if line.startswith("#") or "\t" not in line:
                continue
            k, q = line.rstrip("\n").split("\t", 1)
            for r in pubmed.summary(pubmed.search(q, a.max)):
                h = hits.setdefault(r["pmid"], dict(r, queries=[])); h["queries"].append(k)
            print(f"  {k}: done", file=sys.stderr)
        rows = sorted(hits.values(), key=lambda r: (-len(r["queries"]), -int(r["year"] or 0)))
        with open(d / "candidates.tsv", "w") as f:
            f.write("in_map\tn_queries\tpmid\tyear\tjournal\tfirst_author\ttitle\tqueries\n")
            for r in rows:
                f.write("\t".join(["yes" if r["pmid"] in have else "no", str(len(r["queries"])), r["pmid"], r["year"], r["journal"], r["first_author"], r["title"], ",".join(r["queries"])]) + "\n")
        print(f"{len(rows)} candidates ({sum(r['pmid'] not in have for r in rows)} not yet in the map) -> {d / 'candidates.tsv'}")
    elif a.sub == "merge":
        seen, out = {}, []
        for p in sorted(glob.glob(str(d / "raw" / "*.jsonl"))):
            for r in load_jsonl(p):
                key = str(r.get("pmid") or "") or (r.get("doi") or "").lower() or re.sub(r"\W+", "", r.get("title", "").lower())[:60]
                if key in seen:
                    old = seen[key]
                    for f in ("themes", "modality", "validation"):
                        old[f] = sorted(set(old.get(f) or []) | set(r.get(f) or []))
                    continue
                r["source_file"] = os.path.basename(p); seen[key] = r; out.append(r)
        out.sort(key=lambda r: (str(r.get("year", "")), r.get("first_author", "")))
        with open(d / "papers.jsonl", "w") as f:
            for r in out:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        from collections import Counter
        print(f"{len(out)} papers -> {d / 'papers.jsonl'}")
        for name, key in (("verified", lambda r: [r.get("verified", "?")]), ("type", lambda r: [r.get("type", "?")]), ("year", lambda r: [str(r.get("year", "?"))]), ("themes", lambda r: r.get("themes") or [])):
            c = Counter(x for r in out for x in key(r))
            print(f"  {name}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:18]))
    elif a.sub == "verify":
        os.execv(sys.executable, [sys.executable, str(HOME / "scripts" / "pubmed.py"), "verify", str(d / "papers.jsonl")])
    elif a.sub == "html":
        papers = load_jsonl(d / "papers.jsonl"); meta = json.loads((d / "field.json").read_text()) if (d / "field.json").exists() else {"title": a.slug}
        tpl = (HOME / "templates" / "field_map.html").read_text()
        mapmd = (d / "field_map.md").read_text() if (d / "field_map.md").exists() else ""
        out = tpl.replace("__TITLE__", html.escape(meta.get("title", a.slug))).replace("__DATA__", json.dumps(papers, ensure_ascii=False).replace("</", "<\\/")).replace("__MAP__", json.dumps(mapmd).replace("</", "<\\/"))
        (d / "field_map.html").write_text(out)
        print("wrote", d / "field_map.html", f"({len(papers)} papers)")


STUDIO = str(HOME / "studio" / "folio.py")


def cmd_paper(a):
    sys.exit(subprocess.call([sys.executable, STUDIO, "--studio", os.path.join(os.path.abspath(a.dir), ".studio"), "paper", "init", a.dir, "--journal", a.journal,
                              "--title", a.title, "--figures", str(a.figures), "--supp", str(a.supp)]))


CELL_TOOLS = {
    "figure": "cell-figure/scripts/validate_cell_figure.py",
    "demo": "cell-figure/scripts/cell_templates.py",
    "text": "cell-writing/scripts/cell_text_check.py",
    "legends": "cell-statistics/scripts/legend_stats_check.py",
    "response": "cell-response/scripts/check_response_package.py",
    "refs": "cell-citation/scripts/cell_refs.py",
}


def cmd_cell(a):
    """jf cell <tool> ...  ->  Journal Factory's own Cell skills (cell-skills/)."""
    import subprocess
    root = Path(__file__).resolve().parents[1] / "cell-skills"
    if a.tool == "list" or a.tool not in CELL_TOOLS:
        print("Cell skills:", root)
        for k, v in CELL_TOOLS.items():
            print(f"  jf cell {k:<9} {v}{'' if (root / v).is_file() else '   (missing)'}")
        print("  rules: cell-shared/journal-formats/cell.md")
        return 0 if a.tool == "list" else 2
    script = root / CELL_TOOLS[a.tool]
    if not script.is_file():
        print(f"missing: {script}"); return 2
    return subprocess.call([sys.executable, str(script)] + (["--demo"] if a.tool == "demo" and a.rest and not a.rest[0].startswith("-") else []) + a.rest)


def cmd_doctor(a):
    ok = lambda b: "ok     " if b else "MISSING"
    print("Journal Factory at", HOME)
    print(" ", ok(len(journals()) > 0), f"journal profiles: {len(journals())}")
    for v in ("nature-skills", "cell-skills", "cancer-cell-skills", "k-dense", "biocartoon", "schematic-figure", "paperlens"):
        print(" ", ok((HOME / "vendor" / v).is_dir()), "vendor/" + v)
    print(" ", ok(os.path.exists(STUDIO)), "built-in studio (writing + figure editor): bin/jf-studio")
    print(" ", ok(os.path.exists(os.path.expanduser("~/.claude/skills/omics-report-studio/SKILL.md"))), "omics-report-studio (journal-plan report)")
    for t in ("pdfinfo", "pdffonts", "pdftotext"):
        print(" ", ok(shutil.which(t)), t, "(figure check for PDF)")
    for m in ("PIL", "matplotlib"):
        try:
            __import__(m); print("  ok     ", m)
        except Exception:
            print("  MISSING", m)
    print(" ", ok((HOME / "tools" / "biocartoon_env" / "bin" / "biocartoon").exists()), "BioCartoon (built in): bin/jf-cartoon")
    fields = [p.name for p in (HOME / "fields").glob("*") if p.is_dir()] if (HOME / "fields").exists() else []
    print("  fields:", ", ".join(fields) or "none")


def main():
    ap = argparse.ArgumentParser(prog="jf", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("journals").set_defaults(f=cmd_journals)
    p = sp.add_parser("journal"); p.add_argument("id"); p.set_defaults(f=cmd_journal)
    p = sp.add_parser("compare"); p.add_argument("ids", nargs="+"); p.set_defaults(f=cmd_compare)
    p = sp.add_parser("fit"); p.add_argument("paper"); p.add_argument("--scenario"); p.set_defaults(f=cmd_fit)
    p = sp.add_parser("count"); p.add_argument("file"); p.add_argument("--journal", required=True); p.set_defaults(f=cmd_count)
    p = sp.add_parser("check-figure"); p.add_argument("file"); p.add_argument("--journal", required=True); p.add_argument("--width"); p.set_defaults(f=cmd_check_figure)
    p = sp.add_parser("field"); p.add_argument("sub", choices=["init", "scan", "merge", "verify", "html"]); p.add_argument("slug"); p.add_argument("--title"); p.add_argument("--max", type=int, default=40); p.set_defaults(f=cmd_field)
    p = sp.add_parser("paper"); p.add_argument("sub", choices=["init"]); p.add_argument("dir"); p.add_argument("--journal", required=True); p.add_argument("--title", required=True)
    p.add_argument("--figures", type=int, default=7); p.add_argument("--supp", type=int, default=0); p.set_defaults(f=cmd_paper)
    p = sp.add_parser("cell"); p.add_argument("tool"); p.add_argument("rest", nargs=argparse.REMAINDER); p.set_defaults(f=cmd_cell)
    sp.add_parser("doctor").set_defaults(f=cmd_doctor)
    if len(sys.argv) > 1 and sys.argv[1] == "cartoon":
        sys.exit(subprocess.call([str(HOME / "bin" / "jf-cartoon")] + sys.argv[2:]))
    if len(sys.argv) > 1 and sys.argv[1] == "studio":
        sys.exit(subprocess.call([sys.executable, STUDIO] + sys.argv[2:]))
    a = ap.parse_args()
    r = a.f(a)
    sys.exit(r or 0)


if __name__ == "__main__":
    main()
