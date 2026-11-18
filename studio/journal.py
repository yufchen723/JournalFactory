"""Journal profiles and checks for Folio Studio's paper mode (0.6.0). Stdlib only (PIL used when present).

Profiles are JSON files (one per journal) looked up in: <studio>/journals, $FOLIO_JOURNALS, <skill>/journals.
A folio carries its journal in doc["journal"] (profile id) and, for a manuscript, doc["paper"] = {"role": ..., "n": ...}.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def journal_dirs(studio=None):
    out = []
    if studio:
        out.append(os.path.join(studio, "journals"))
    if os.environ.get("FOLIO_JOURNALS"):
        out.append(os.environ["FOLIO_JOURNALS"])
    out.append(os.path.join(os.path.dirname(HERE), "journals"))
    return [d for d in out if os.path.isdir(d)]


def journals(studio=None):
    out = {}
    for d in reversed(journal_dirs(studio)):          # earlier dirs win
        for f in sorted(os.listdir(d)):
            if f.endswith(".json") and not f.startswith("_"):
                try:
                    j = json.load(open(os.path.join(d, f)))
                    out[j.get("id", f[:-5])] = j
                except Exception:
                    pass
    return out


def summary(j):
    L, F = j["limits"], j["figure"]
    return {"id": j["id"], "name": j["name"], "tier": j.get("tier"), "widths_mm": F["widths_mm"], "max_height_mm": F["max_height_mm"], "font_pt": F["font_pt"],
            "panel_label": F["panel_label"], "main_display_items": L.get("main_display_items"), "main_text_words": L.get("main_text_words"),
            "abstract_words": L.get("abstract_words"), "verified": j["verified"]["level"]}


def words(t):
    t = re.sub(r"<[^>]+>|\[\^?\d+\]|[*_`#>|]", " ", t or "")
    return len(re.findall(r"[A-Za-z0-9][\w'’\-/.%]*", t))


KIND = {"summary": "abstract", "abstract": "abstract", "in brief": "etoc", "etoc": "etoc", "etoc blurb": "etoc", "highlights": "highlights",
        "star methods": "methods", "methods": "methods", "materials and methods": "methods", "online methods": "methods", "references": "references",
        "supplemental information": "skip", "acknowledgments": "skip", "acknowledgements": "skip", "author contributions": "skip", "declaration of interests": "skip",
        "competing interests": "skip", "data availability": "skip", "code availability": "skip", "resource availability": "skip", "keywords": "skip", "title": "skip",
        "authors": "skip", "title)": "skip", "authors and affiliations": "skip", "graphical abstract": "skip"}


def _img_px(path):
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def check(doc, j, folio_dir=None):
    """Return {"journal", "verified", "items": [{level: error|warn|ok|info, block, msg}], "counts": {...}}."""
    F, L = j["figure"], j["limits"]
    items = []
    add = lambda level, msg, block=None: items.append({"level": level, "msg": msg, "block": block})
    blocks = [b for b in doc.get("blocks", []) if not b.get("hidden")]
    role = (doc.get("paper") or {}).get("role", "")
    counts = {}
    if doc.get("mode") == "canvas" and role != "graphical_abstract":
        w, h = doc["page"]["w_mm"], doc["page"]["h_mm"]
        near = min(F["widths_mm"].items(), key=lambda kv: abs(kv[1] - w))
        if abs(near[1] - w) > 0.6:
            add("error", f"Page width {w:g} mm is not a {j['name']} width ({', '.join(f'{k} {v}' for k, v in F['widths_mm'].items())} mm).")
        else:
            add("ok", f"Page width {w:g} mm = {near[0]} column.")
        if h > F["max_height_mm"] + 0.5:
            add("error", f"Page height {h:g} mm exceeds {F['max_height_mm']} mm.")
        lo, hi = F["font_pt"]["min"], F["font_pt"]["max"]; PL = F["panel_label"]
        default_pt = (doc.get("style") or {}).get("text_pt", 8)
        fams = [x.lower() for x in F["font_family"]]
        labels = []
        for b in blocks:
            if b.get("type") == "text":
                pt = b.get("pt", default_pt); txt = re.sub(r"[*_]", "", b.get("text", "")).strip()
                if b.get("role") == "label" or re.fullmatch(r"[A-Za-z]", txt):
                    labels.append(txt)
                    if abs(pt - PL["pt"]) > 0.25:
                        add("warn", f"Panel letter {txt}: {pt:g} pt; {j['name']} uses {PL['pt']} pt bold.", b["id"])
                    if txt and (txt.isupper() != (PL["case"] == "upper")):
                        add("error", f"Panel letter {txt}: {j['name']} uses {'capital' if PL['case'] == 'upper' else 'lower-case'} letters.", b["id"])
                    continue
                if b.get("role") in ("title", "legend"):
                    continue
                if pt < lo - 0.01:
                    add("error", f"Text {pt:g} pt is below the {lo} pt minimum.", b["id"])
                elif pt > hi + 0.01:
                    add("warn", f"Text {pt:g} pt is above the {hi} pt figure range.", b["id"])
                fam = (b.get("font") or (doc.get("style") or {}).get("font", "")).lower()
                if fam and not any(x in fam for x in fams):
                    add("warn", f"Font {b.get('font')} is not {' / '.join(F['font_family'])}.", b["id"])
                for m in re.finditer(r"font-size:\s*([\d.]+)pt", b.get("html", "") or ""):
                    if float(m.group(1)) < lo - 0.01:
                        add("error", f"Inline text {float(m.group(1)):g} pt is below {lo} pt.", b["id"]); break
            elif b.get("type") == "image":
                src = b.get("src", ""); ext = src.lower().rsplit(".", 1)[-1]
                if b.get("x", 0) < -0.1 or b.get("y", 0) < -0.1 or b.get("x", 0) + b.get("w", 0) > w + 0.1 or b.get("y", 0) + b.get("h", 0) > h + 0.1:
                    add("error", "Panel extends beyond the page.", b["id"])
                if ext in ("png", "jpg", "jpeg", "tif", "tiff", "webp") and folio_dir:
                    px = _img_px(os.path.join(folio_dir, src))
                    if px and b.get("w"):
                        c = b.get("crop") or {}
                        vis = px[0] * (1 - c.get("l", 0) - c.get("r", 0))
                        dpi = vis / (b["w"] / 25.4); need = F["dpi"].get("photo", 300)
                        if dpi < need - 1:
                            add("error", f"Raster panel is {dpi:.0f} dpi at this size; needs {need} dpi (re-export larger or as vector).", b["id"])
                        else:
                            add("info", f"Raster panel {dpi:.0f} dpi. Text inside a raster panel cannot be checked or edited.", b["id"])
            elif b.get("type") == "shape" and b.get("stroke") not in (None, "none") and b.get("sw") is not None:
                if b["sw"] < F["line_pt"]["min"] - 0.01:
                    add("warn", f"Line {b['sw']:g} pt is thinner than {F['line_pt']['min']} pt.", b["id"])
        seq = [x.lower() for x in labels if x]
        exp = [chr(97 + i) for i in range(len(seq))]
        if seq and sorted(seq) != exp:
            add("warn", f"Panel letters are {', '.join(labels)}; expected a continuous run from {'A' if PL['case'] == 'upper' else 'a'}.")
        counts["panels"] = len([b for b in blocks if b.get("type") == "image"])
    elif doc.get("mode") == "flow":
        cur, secs, order = "(front)", {}, []
        for b in blocks:
            if b.get("type") != "text":
                continue
            t = b.get("text", "")
            m = re.match(r"^#{1,2}\s+(.*)", t.strip())
            if m:
                cur = "(title)" if t.strip().startswith("# ") else m.group(1).strip()
                if cur not in secs:
                    order.append(cur)
                secs.setdefault(cur, []); rest = "\n".join(t.strip().split("\n")[1:])
                if rest.strip():
                    secs[cur].append((b["id"], rest))
            else:
                secs.setdefault(cur, []).append((b["id"], t))
        main = 0; per = []
        for name in order:
            kind = "skip" if name == "(title)" else KIND.get(re.sub(r"[^a-z ]", "", name.lower()).strip(), "main")
            body = "\n".join(t for _, t in secs[name]); n = words(body); first = secs[name][0][0] if secs[name] else None
            per.append({"section": name, "kind": kind, "words": n})
            if kind == "abstract" and L.get("abstract_words"):
                add("error" if n > L["abstract_words"] else "ok", f"{name}: {n} words (limit {L['abstract_words']}).", first)
            elif kind == "etoc" and L.get("etoc_words"):
                add("error" if n > L["etoc_words"] else "ok", f"{name}: {n} words (limit {L['etoc_words']}).", first)
            elif kind == "highlights" and L.get("highlights"):
                bl = [re.sub(r"^\s*[-*•]\s*", "", x).strip() for x in body.splitlines() if re.match(r"^\s*[-*•]", x)]
                H = L["highlights"]
                if len(bl) > H["n"]:
                    add("error", f"{len(bl)} highlights (limit {H['n']}).", first)
                for x in bl:
                    if len(x) > H["chars"]:
                        add("error", f"Highlight is {len(x)} characters (limit {H['chars']}): “{x[:50]}…”", first)
                if bl and len(bl) <= H["n"] and all(len(x) <= H["chars"] for x in bl):
                    add("ok", f"{len(bl)} highlights, longest {max(len(x) for x in bl)} characters.", first)
            elif kind == "methods" and (j.get("methods") or {}).get("word_limit"):
                wl = j["methods"]["word_limit"]; add("error" if n > wl else "ok", f"{name}: {n} words (limit {wl}).", first)
            elif kind == "references" and L.get("references"):
                nr = len(re.findall(r"(?m)^\s*\d+\.\s", body))
                if nr:
                    add("warn" if nr > L["references"] else "ok", f"{nr} references (guide: about {L['references']}).", first)
            elif kind == "main":
                main += n
        counts.update({"main_text_words": main, "sections": per})
        lim = L.get("main_text_words")
        if lim and order and role in ("main_text", ""):
            add("error" if main > lim else "ok", f"Main text {main} words (limit about {lim}" + (f"; {L['main_text_counts']}" if L.get("main_text_counts") else "") + ").")
        need = [s for s in j.get("sections", []) if KIND.get(re.sub(r"\s*\(.*", "", s).lower(), "main") != "skip"]
        have = " | ".join(o.lower() for o in order)
        missing = [s for s in need if re.sub(r"\s*\(.*", "", s).lower() not in have and "legend" not in s.lower() and "extended" not in s.lower()]
        if order and missing and role in ("main_text", ""):
            add("info", "Sections not found yet: " + ", ".join(missing) + ".")
    if role == "graphical_abstract":
        add("info", "Graphical abstract: square page; export at 1200 × 1200 px, 300 dpi (Cell Press).")
    add("info", f"Rules verified: {j['verified']['level']}. {j['verified'].get('note', '')}")
    return {"journal": j["id"], "name": j["name"], "verified": j["verified"]["level"], "items": items, "counts": counts,
            "errors": sum(i["level"] == "error" for i in items), "warnings": sum(i["level"] == "warn" for i in items)}


def manuscript_md(j, title):
    """Starter main-text Markdown in the journal's section order."""
    L = j["limits"]; out = [f"# {title}", "", "Authors · affiliations · lead contact", ""]
    hints = {"summary": f"One paragraph, at most {L.get('abstract_words')} words, no citations: context, gap, what was done, findings with numbers, meaning.",
             "abstract": f"At most {L.get('abstract_words')} words, no citations: context, gap, what was done, findings with numbers, meaning.",
             "introduction": "Four paragraphs: the problem · what is known · the gap · what this paper does.",
             "introduction (no heading)": "Four paragraphs: the problem · what is known · the gap · what this paper does.",
             "results": "One sub-heading per figure, written as a declarative sentence.",
             "discussion": "What changes · relation to named prior work · what follows.",
             "limitations of the study": "What the data cannot show, stated plainly.",
             "figure legends": "Figure 1. Title sentence. (A) … n, unit, test, error bars.",
             "star methods": "Key resources table · Experimental model and study participant details · Method details · Quantification and statistical analysis.",
             "methods": "Enough detail to reproduce; statistics and replicate unit stated.",
             "resource availability": "Lead contact · Materials availability · Data and code availability (accession numbers).",
             "references": "1. …"}
    for s in j.get("sections", []):
        k = s.lower()
        if k in ("title", "authors", "authors and affiliations"):
            continue
        out += [f"## {re.sub(r' *[(]no heading[)]', '', s)}", "", hints.get(k, "…"), ""]
        if k in ("summary", "abstract") and L.get("highlights"):
            pass
    return "\n".join(out)


def front_md(j):
    L = j["limits"]; out = []
    if L.get("highlights"):
        out += ["## Highlights", ""] + [f"- Highlight {i + 1} (at most {L['highlights']['chars']} characters)" for i in range(L["highlights"]["n"])] + [""]
    if L.get("etoc_words"):
        out += ["## In brief", "", f"Two sentences, third person, at most {L['etoc_words']} words.", ""]
    out += ["## Title options", "", "1. …", "", "## Cover letter", "", "What is new · why this journal · related manuscripts · suggested and excluded reviewers.", ""]
    return "\n".join(out)
