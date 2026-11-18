#!/usr/bin/env python3
"""Check exported figure files against Cell's production rules.

Rules: cell-shared/journal-formats/cell.md section 5 (figures) and section 6 (graphical
abstract), read on cell.com 2026-11-18.

    validate_cell_figure.py "Figure 1.pdf" "Figure 1.tiff"
    validate_cell_figure.py fig.pdf --stage initial        # report only; nothing blocks
    validate_cell_figure.py GA.tiff --ga                    # graphical abstract rules
    validate_cell_figure.py fig.tiff --kind lineart         # 1,000 dpi rule
    validate_cell_figure.py fig.pdf --json report.json --strict

PDF checks are done by reading the file directly (no extra packages): page size, fonts
and embedding, text sizes, stroke widths, colour space, red with green, gray fills, and the
resolution of every placed image. Raster files need Pillow.

Levels: FAIL = breaks a stated Cell rule; WARN = outside a recommendation or needs a look;
INFO = for the record. Exit code 1 on FAIL (and on WARN with --strict), 2 when a file cannot
be read. The audit never replaces looking at the figure at its printed size.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
import zlib
from pathlib import Path

WIDTHS_MM = {"1 column": 85.0, "1.5 columns": 114.0, "full width": 174.0}
REC_MAX_MM = (165.0, 200.0)
PAGE_MAX_MM = 279.4          # a figure must fit on one page (US Letter height)
TEXT_PT = (6.0, 8.0)
TEXT_HARD_FLOOR = 5.0        # below this the text is unreadable in print; Cell says "about 6-8 pt"
STROKE_PT = (0.5, 1.5)
DPI = {"colour": 300, "grayscale": 300, "bw": 500, "lineart": 1000}
MAX_MB = 20.0
GA = {"px": 1200, "dpi": 300, "text_pt": (8.0, 12.0), "formats": (".tif", ".tiff", ".pdf", ".jpg", ".jpeg")}
PREFERRED = (".tif", ".tiff", ".pdf")
ACCEPTED = PREFERRED + (".eps", ".jpg", ".jpeg", ".psd", ".png", ".cdx")
ARIAL = re.compile(r"arial", re.I)
ARIAL_LIKE = re.compile(r"liberationsans|helvetica|nimbussan|arimo", re.I)

PT_MM = 25.4 / 72


def _load_profile() -> None:
    """Use Journal Factory's journals/cell.json when it is present, so there is one source of numbers."""
    global TEXT_PT, STROKE_PT, MAX_MB
    for p in Path(__file__).resolve().parents[:5]:
        f = p / "journals" / "cell.json"
        if f.is_file():
            try:
                F = json.loads(f.read_text())["figure"]
                for k, v in zip(("1 column", "1.5 columns", "full width"), (F["widths_mm"][x] for x in ("single", "mid", "double"))):
                    WIDTHS_MM[k] = float(v)
                TEXT_PT = (float(F["font_pt"]["min"]), float(F["font_pt"]["max"]))
                STROKE_PT = (float(F["line_pt"]["min"]), float(F["line_pt"]["max"]))
                MAX_MB = float(F.get("max_file_mb", MAX_MB))
            except Exception:
                pass
            return


_load_profile()


def F(level: str, check: str, msg: str) -> dict:
    return {"level": level, "check": check, "message": msg}


# ----------------------------------------------------------------------------- PDF

_STREAM = re.compile(rb"stream\r?\n")
_TOKEN = re.compile(
    rb"%[^\r\n]*|\((?:\\.|[^\\()])*\)|<<|>>|<[0-9A-Fa-f\s]*>|[\[\]]|/[^\s/<>\[\]()%]*"
    rb"|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?|[^\s/<>\[\]()%]+", re.S)
_NUM = re.compile(rb"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?$")
_I = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _mul(m, n):
    a, b, c, d, e, f = m; A, B, C, D, E, Fv = n
    return (a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D, e * A + f * C + E, e * B + f * D + Fv)


def _scale(m) -> float:
    return abs(m[0] * m[3] - m[1] * m[2]) ** 0.5


def _streams(data: bytes):
    """Yield (dictionary bytes, decoded payload or None) for every stream object."""
    pos = 0
    while True:
        m = _STREAM.search(data, pos)
        if not m:
            return
        end = data.find(b"endstream", m.end())
        if end < 0:
            return
        head = data[max(0, m.start() - 4096):m.start()]
        i = head.rfind(b" obj")
        d = head[i:] if i >= 0 else head
        payload = data[m.end():end]
        if b"/FlateDecode" in d:
            try:
                payload = zlib.decompress(payload)
            except zlib.error:
                try:
                    payload = zlib.decompressobj().decompress(payload)
                except zlib.error:
                    payload = None
        elif b"/Filter" in d:
            payload = None
        yield d, payload
        pos = end + 9


def _objects(data: bytes) -> dict:
    """Object number -> raw bytes, including objects packed in object streams."""
    out = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", data, re.S):
        out[int(m.group(1))] = m.group(2)
    for d, payload in _streams(data):
        if b"/ObjStm" in d and payload:
            n = re.search(rb"/N\s+(\d+)", d); first = re.search(rb"/First\s+(\d+)", d)
            if not (n and first):
                continue
            nums = payload[:int(first.group(1))].split()
            pairs = [(int(nums[i]), int(nums[i + 1])) for i in range(0, min(len(nums) - 1, 2 * int(n.group(1))), 2)]
            body = payload[int(first.group(1)):]
            for k, (num, off) in enumerate(pairs):
                stop = pairs[k + 1][1] if k + 1 < len(pairs) else len(body)
                out.setdefault(num, body[off:stop])
    return out


def _scan_content(stream: bytes, st: dict) -> None:
    """Walk one content stream: text sizes, stroke widths, colours, image placements."""
    ops: list[bytes] = []
    ctm = _I; stack = []; tm = _I; fsize = 0.0; font = ""; lw = 1.0
    gstack = []
    for m in _TOKEN.finditer(stream):
        t = m.group(0)
        if t.startswith(b"%"):
            continue
        if t.startswith(b"("):
            ops.append(b"("); continue
        if t[:1] in (b"/", b"[", b"]", b"<") or _NUM.match(t):
            ops.append(t); continue
        try:
            if t == b"q":
                stack.append(ctm); gstack.append(lw)
            elif t == b"Q":
                if stack:
                    ctm = stack.pop()
                if gstack:
                    lw = gstack.pop()
            elif t == b"cm" and len(ops) >= 6:
                ctm = _mul(tuple(float(x) for x in ops[-6:]), ctm)
            elif t == b"BT":
                tm = _I
            elif t == b"Tm" and len(ops) >= 6:
                tm = tuple(float(x) for x in ops[-6:])
            elif t == b"Tf" and len(ops) >= 2:
                font = ops[-2].lstrip(b"/").decode("ascii", "replace"); fsize = float(ops[-1])
            elif t in (b"Tj", b"TJ", b"'", b'"'):
                s = abs(fsize) * _scale(_mul(tm, ctm))
                if s > 0:
                    st["text"].append((round(s, 2), font))
            elif t == b"w" and ops:
                lw = float(ops[-1])
            elif t in (b"S", b"s", b"B", b"b", b"B*", b"b*"):
                st["strokes"].append(round(lw * _scale(ctm), 3))
            elif t in (b"rg", b"RG") and len(ops) >= 3:
                rgb = tuple(float(x) for x in ops[-3:])
                st["rgb_fill" if t == b"rg" else "rgb_stroke"].add(tuple(round(v, 3) for v in rgb))
            elif t in (b"g", b"G") and ops:
                v = round(float(ops[-1]), 3)
                st["rgb_fill" if t == b"g" else "rgb_stroke"].add((v, v, v))
            elif t in (b"k", b"K"):
                st["cmyk"] = True
            elif t == b"Do" and ops:
                st["do"].append((ops[-1].lstrip(b"/").decode("ascii", "replace"), abs(ctm[0]) or _scale(ctm), abs(ctm[3]) or _scale(ctm)))
        except ValueError:
            pass
        ops.clear()


def audit_pdf(path: Path, kind: str = "colour", ga: bool = False) -> list[dict]:
    out: list[dict] = []
    data = path.read_bytes()
    if not data.startswith(b"%PDF"):
        return [F("FAIL", "file", "not a PDF")]
    objs = _objects(data)
    blob = b"\n".join(objs.values()) if objs else data

    # pages and size
    pages = [o for o in objs.values() if re.search(rb"/Type\s*/Page(?![s\w])", o)]
    if len(pages) != 1:
        out.append(F("FAIL" if len(pages) > 1 else "WARN", "pages", f"{len(pages)} pages found; one figure = one page with all panels"))
    box = None
    for o in pages or [blob]:
        m = re.search(rb"/(?:CropBox|MediaBox)\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]", o) or \
            re.search(rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]", blob)
        if m:
            x0, y0, x1, y1 = (float(v) for v in m.groups()); box = ((x1 - x0) * PT_MM, (y1 - y0) * PT_MM); break
    if box:
        out += _size_findings(box[0], box[1], ga)
    else:
        out.append(F("WARN", "size", "page size not found"))

    # fonts
    names = sorted({m.group(1).decode("latin1") for m in re.finditer(rb"/BaseFont\s*/([^\s/<>\[\]()]+)", blob)})
    clean = sorted({re.sub(r"^[A-Z]{6}\+", "", n) for n in names})
    type3 = len(re.findall(rb"/Subtype\s*/Type3", blob))
    embedded = len(re.findall(rb"/FontFile[23]?\s", blob))
    descriptors = len(re.findall(rb"/Type\s*/FontDescriptor", blob))
    if type3:
        out.append(F("FAIL", "fonts", f"{type3} Type 3 font(s): text was converted to drawings and cannot be edited or typeset (set pdf.fonttype 42 / use cairo_pdf)"))
    not_arial = [n for n in clean if not ARIAL.search(n)]
    if not clean and not type3:
        out.append(F("WARN", "fonts", "no fonts found: all text is outlines or inside images (cannot be checked or edited)"))
    elif not_arial:
        like = [n for n in not_arial if ARIAL_LIKE.search(n)]
        other = [n for n in not_arial if n not in like]
        if other:
            out.append(F("FAIL", "fonts", f"fonts other than Arial: {', '.join(other)} (Cell: use only Arial)"))
        if like:
            out.append(F("WARN", "fonts", f"Arial substitute in use: {', '.join(like)}. Same metrics, but re-export with Arial before the production upload"))
    else:
        out.append(F("INFO", "fonts", f"Arial only ({', '.join(clean)})"))
    if descriptors and embedded < descriptors:
        out.append(F("FAIL", "fonts", f"{descriptors - embedded} of {descriptors} fonts are not embedded (Cell: always embed fonts)"))

    # content
    st = {"text": [], "strokes": [], "rgb_fill": set(), "rgb_stroke": set(), "cmyk": False, "do": []}
    unread = 0
    for d, payload in _streams(data):
        if any(k in d for k in (b"/Subtype /Image", b"/Subtype/Image", b"/FontFile", b"/ObjStm", b"/XRef", b"/Length1", b"/Type /Metadata")):
            continue
        if payload is None:
            unread += 1; continue
        if b"BT" in payload or b" re" in payload or b" l\n" in payload or b" m\n" in payload or b"Do" in payload:
            _scan_content(payload, st)
    if unread:
        out.append(F("WARN", "content", f"{unread} stream(s) use a filter this script cannot read; those parts are not checked"))

    lo, hi = GA["text_pt"] if ga else TEXT_PT
    sizes = sorted({s for s, _ in st["text"]})
    if sizes:
        small = [s for s in sizes if s < lo - 0.05]; big = [s for s in sizes if s > hi + 0.05]
        hard = [s for s in small if s < TEXT_HARD_FLOOR]
        if hard and not ga:
            out.append(F("FAIL", "text size", f"text at {', '.join(f'{s:g}' for s in hard)} pt: too small to print (Cell: about {lo:g}-{hi:g} pt)"))
        rest = [s for s in small if s not in hard] if not ga else small
        if rest:
            out.append(F("FAIL" if ga else "WARN", "text size", f"text below {lo:g} pt: {', '.join(f'{s:g}' for s in rest)} pt (often superscripts or tick labels)"))
        if big:
            out.append(F("WARN", "text size", f"text above {hi:g} pt: {', '.join(f'{s:g}' for s in big)} pt (Cell: about {lo:g}-{hi:g} pt)"))
        if not small and not big:
            out.append(F("INFO", "text size", f"all text {sizes[0]:g}-{sizes[-1]:g} pt"))
    elif clean:
        out.append(F("WARN", "text size", "fonts are present but no text runs could be measured"))

    if st["strokes"] and not ga:
        slo, shi = STROKE_PT
        thin = sorted({s for s in st["strokes"] if 0 <= s < slo - 0.02}); thick = sorted({s for s in st["strokes"] if s > shi + 0.02})
        n = len(st["strokes"])
        if thin:
            k = sum(1 for s in st["strokes"] if s < slo - 0.02)
            out.append(F("WARN", "strokes", f"{k} of {n} strokes thinner than {slo:g} pt (widths: {', '.join(f'{s:g}' for s in thin[:6])}); marker outlines count too, axes and data lines must not be thinner"))
        if thick:
            k = sum(1 for s in st["strokes"] if s > shi + 0.02)
            out.append(F("WARN", "strokes", f"{k} of {n} strokes thicker than {shi:g} pt (widths: {', '.join(f'{s:g}' for s in thick[:6])}); fine for scale bars and data emphasis, not for axes"))
        if not thin and not thick:
            out.append(F("INFO", "strokes", f"{n} strokes, all {slo:g}-{shi:g} pt"))

    if st["cmyk"] or b"/DeviceCMYK" in blob:
        out.append(F("FAIL", "colour", "CMYK colour found (Cell: colour is encoded as RGB)"))
    cols = st["rgb_fill"] | st["rgb_stroke"]
    kinds = {_hue(c) for c in cols}
    if {"red", "green"} <= kinds:
        out.append(F("WARN", "colour", "red and green are both used in vector elements (Cell: do not use them together)"))
    out += _gray_findings(st["rgb_fill"])

    # images
    img = {}
    for num, o in objs.items():
        if re.search(rb"/Subtype\s*/Image", o):
            w = re.search(rb"/Width\s+(\d+)", o); h = re.search(rb"/Height\s+(\d+)", o)
            if w and h:
                img[num] = (int(w.group(1)), int(h.group(1)), b"/DeviceCMYK" in o)
    name2obj = {m.group(1).decode("latin1"): int(m.group(2)) for m in re.finditer(rb"/([A-Za-z0-9_.\-]+)\s+(\d+)\s+0\s+R", blob) if int(m.group(2)) in img}
    need = DPI[kind]
    placed = 0
    for name, wpt, hpt in st["do"]:
        if name not in name2obj or wpt <= 0:
            continue
        wpx, hpx, cmyk = img[name2obj[name]]
        placed += 1
        dpi = min(wpx / (wpt / 72), hpx / (hpt / 72)) if hpt > 0 else wpx / (wpt / 72)
        if min(wpx, hpx) <= 8:
            out.append(F("INFO", "image resolution", f"image {name}: {wpx}x{hpx} px colour gradient (a colour bar); not a data image"))
        elif dpi < need - 1:
            out.append(F("FAIL", "image resolution", f"image {name}: {wpx}x{hpx} px placed at {wpt * PT_MM:.1f}x{hpt * PT_MM:.1f} mm = {dpi:.0f} dpi (needs {need})"))
        else:
            out.append(F("INFO", "image resolution", f"image {name}: {dpi:.0f} dpi at {wpt * PT_MM:.1f} mm wide"))
    if img and not placed:
        out.append(F("WARN", "image resolution", f"{len(img)} embedded image(s) whose placed size could not be read; check them by hand"))
    if not img:
        out.append(F("INFO", "image resolution", "no raster images: vector only"))
    return out


def _hue(c) -> str | None:
    h, s, v = colorsys.rgb_to_hsv(*c)
    if s < 0.35 or v < 0.25:
        return None
    d = h * 360
    return "red" if d < 30 or d >= 340 else "green" if 80 <= d < 170 else None


def _gray_findings(fills) -> list[dict]:
    grays = sorted({round(1 - c[0], 2) for c in fills if abs(c[0] - c[1]) < 0.01 and abs(c[1] - c[2]) < 0.01 and 0.005 < c[0] < 0.995})
    out = []
    if not grays:
        return out
    light = [g for g in grays if g < 0.10 - 1e-6]; dark = [g for g in grays if g > 0.80 + 1e-6]
    close = [(a, b) for a, b in zip(grays, grays[1:]) if b - a < 0.20 - 1e-6]
    msg = []
    if light:
        msg.append(f"lighter than 10%: {', '.join(f'{g:.0%}' for g in light)}")
    if dark:
        msg.append(f"darker than 80%: {', '.join(f'{g:.0%}' for g in dark)}")
    if close:
        msg.append("less than 20% apart: " + ", ".join(f"{a:.0%}/{b:.0%}" for a, b in close[:4]))
    if msg:
        out.append(F("WARN", "gray fills", "gray fills (as % black) " + "; ".join(msg) + ". Applies to filled areas; gray text and axes also appear here"))
    return out


def _size_findings(w: float, h: float, ga: bool) -> list[dict]:
    out = []
    if ga:
        side = GA["px"] / GA["dpi"] * 25.4
        if abs(w - h) > 0.5:
            out.append(F("FAIL", "size", f"graphical abstract is {w:.1f} x {h:.1f} mm; it must be square"))
        elif abs(w - side) > 1:
            out.append(F("WARN", "size", f"graphical abstract is {w:.1f} mm square; 1200 px at 300 dpi is {side:.1f} mm"))
        else:
            out.append(F("INFO", "size", f"{w:.1f} mm square"))
        return out
    full = WIDTHS_MM["full width"]
    name, near = min(WIDTHS_MM.items(), key=lambda kv: abs(kv[1] - w))
    if w > full + 0.5:
        out.append(F("FAIL", "size", f"width {w:.1f} mm exceeds the full page width ({full:g} mm)"))
    elif abs(near - w) <= 0.5:
        out.append(F("INFO", "size", f"width {w:.1f} mm = {name}"))
    else:
        out.append(F("WARN", "size", f"width {w:.1f} mm is not a Cell column width ({', '.join(f'{v:g}' for v in WIDTHS_MM.values())} mm); it will be resized at typesetting"))
    if h > PAGE_MAX_MM:
        out.append(F("FAIL", "size", f"height {h:.1f} mm does not fit one page"))
    elif h > REC_MAX_MM[1] + 0.5:
        out.append(F("WARN", "size", f"height {h:.1f} mm is above the recommended {REC_MAX_MM[1]:g} mm; the legend may be set on another page"))
    if w > REC_MAX_MM[0] + 0.5 and w <= full + 0.5:
        out.append(F("INFO", "size", f"wider than the recommended {REC_MAX_MM[0]:g} mm; allowed up to {full:g} mm"))
    return out


# ----------------------------------------------------------------------------- raster

def audit_raster(path: Path, kind: str = "colour", ga: bool = False, width_mm: float | None = None) -> list[dict]:
    try:
        from PIL import Image
    except ImportError:
        return [F("WARN", "file", "Pillow is not installed; raster files cannot be checked")]
    Image.MAX_IMAGE_PIXELS = None
    out = []
    im = Image.open(path)
    w, h = im.size
    dpi = im.info.get("dpi", (None, None))[0]
    dpi = float(dpi) if dpi else None
    if ga:
        if (w, h) != (GA["px"], GA["px"]):
            out.append(F("FAIL", "size", f"{w} x {h} px; the graphical abstract is {GA['px']} x {GA['px']} px"))
        else:
            out.append(F("INFO", "size", f"{w} x {h} px"))
        if dpi is None or abs(dpi - GA["dpi"]) > 1:
            out.append(F("WARN", "resolution", f"stored resolution {dpi}; set {GA['dpi']} dpi"))
    else:
        need = DPI[kind]
        if width_mm:
            eff = w / (width_mm / 25.4)
            out += _size_findings(width_mm, h / eff * 25.4, False)
            out.append(F("FAIL" if eff < need - 1 else "INFO", "resolution", f"{w} px across {width_mm:g} mm = {eff:.0f} dpi (needs {need} for {kind})"))
        elif dpi:
            wmm, hmm = w / dpi * 25.4, h / dpi * 25.4
            out += _size_findings(wmm, hmm, False)
            out.append(F("FAIL" if dpi < need - 1 else "INFO", "resolution", f"{dpi:.0f} dpi stored (needs {need} for {kind})"))
        else:
            eff = w / (WIDTHS_MM["full width"] / 25.4)
            out.append(F("WARN", "resolution", f"no resolution stored; at full width ({WIDTHS_MM['full width']:g} mm) this is {eff:.0f} dpi (needs {need}). Pass --width-mm"))
    if im.mode == "CMYK":
        out.append(F("FAIL", "colour", "CMYK image (Cell: RGB)"))
    elif im.mode in ("RGBA", "LA", "PA"):
        out.append(F("WARN", "colour", f"mode {im.mode}: has a transparency channel; flatten onto white (RGB)"))
    elif im.mode in ("RGB", "L", "1", "P"):
        out.append(F("INFO", "colour", f"mode {im.mode}"))
    else:
        out.append(F("WARN", "colour", f"mode {im.mode}: convert to RGB"))
    if getattr(im, "n_frames", 1) > 1:
        out.append(F("WARN", "layers", f"{im.n_frames} pages/layers; flatten to one"))
    if path.suffix.lower() in (".tif", ".tiff"):
        comp = im.info.get("compression", "raw")
        out.append(F("INFO" if comp == "tiff_lzw" else "WARN", "compression", f"TIFF compression: {comp}" + ("" if comp == "tiff_lzw" else " (Cell suggests LZW to keep the file small)")))
    return out


# ----------------------------------------------------------------------------- SVG

def audit_svg(path: Path) -> list[dict]:
    t = path.read_text(errors="replace")
    out = [F("WARN", "format", "SVG is a working format; Cell takes TIFF or PDF (also EPS, JPEG, PNG, PSD). Export a PDF for upload")]
    m = re.search(r"<svg[^>]*?\bwidth=\"([\d.]+)(mm|pt|in|px|cm)?\"[^>]*?\bheight=\"([\d.]+)(mm|pt|in|px|cm)?\"", t, re.S)
    k = {"mm": 1, "cm": 10, "in": 25.4, "pt": PT_MM, "px": 25.4 / 96, None: 25.4 / 96}
    if m:
        out += _size_findings(float(m.group(1)) * k[m.group(2)], float(m.group(3)) * k[m.group(4)], False)
    fams = {f.strip().strip("'\"") for m in re.finditer(r"font-family\s*[:=]\s*[\"']?([^;\"'>]+)", t) for f in m.group(1).split(",")[:1]}
    bad = sorted(f for f in fams if f and not ARIAL.search(f))
    if bad:
        out.append(F("WARN" if all(ARIAL_LIKE.search(b.replace(' ', '')) for b in bad) else "FAIL", "fonts", f"font families other than Arial: {', '.join(bad)}"))
    if "<text" not in t:
        out.append(F("WARN", "fonts", "no <text> elements: text is outlined (set svg.fonttype none)"))
    return out


# ----------------------------------------------------------------------------- driver

def audit_file(path: Path, kind: str = "colour", ga: bool = False, stage: str = "production", width_mm: float | None = None) -> dict:
    path = Path(path)
    res = {"file": str(path), "stage": stage, "kind": "graphical abstract" if ga else kind, "findings": []}
    if not path.is_file():
        res["findings"] = [F("FAIL", "file", "file not found")]; res["verdict"] = "NOT AUDITABLE"; return res
    ext = path.suffix.lower()
    fnd: list[dict] = []
    mb = path.stat().st_size / 1e6
    if ga:
        fnd.append(F("INFO" if ext in GA["formats"] else "FAIL", "format", f"{ext or 'no extension'} (graphical abstract: TIFF, PDF or JPG)"))
    elif ext in PREFERRED:
        fnd.append(F("INFO", "format", f"{ext[1:].upper()} (preferred by Cell)"))
    elif ext in ACCEPTED:
        fnd.append(F("INFO", "format", f"{ext[1:].upper()} is accepted; TIFF and PDF are preferred"))
    elif ext != ".svg":
        fnd.append(F("FAIL", "format", f"{ext} is not a Cell production format (TIFF, PDF, EPS, JPEG, PSD, PNG)"))
    fnd.append(F("FAIL" if mb > MAX_MB else "INFO", "file size", f"{mb:.2f} MB (limit {MAX_MB:g} MB per figure)"))
    try:
        if ext == ".pdf":
            fnd += audit_pdf(path, kind, ga)
        elif ext == ".svg":
            fnd += audit_svg(path)
        elif ext in (".tif", ".tiff", ".png", ".jpg", ".jpeg"):
            fnd += audit_raster(path, kind, ga, width_mm)
        else:
            fnd.append(F("WARN", "file", "this format is not inspected; export a PDF or TIFF to check"))
    except Exception as exc:  # never crash on a strange file
        fnd.append(F("WARN", "file", f"could not be fully read ({type(exc).__name__}: {exc})"))
    if not ga and not re.match(r"^(Figure|Fig)\s?S?\d+\.", path.name, re.I):
        fnd.append(F("INFO", "file name", "Cell asks for clear names such as 'Figure 1.tif'"))
    if stage == "initial":
        for f in fnd:
            if f["level"] in ("FAIL", "WARN"):
                f["message"] += " [needed for production files, not at first submission]"; f["level"] = "LATER"
    res["findings"] = fnd
    lv = {f["level"] for f in fnd}
    res["verdict"] = "FIX BEFORE UPLOAD" if "FAIL" in lv else "REVIEW" if "WARN" in lv else "OK FOR FIRST SUBMISSION" if stage == "initial" else "PASS"
    return res


def render(res: dict) -> str:
    lines = [f"{res['file']}  [{res['kind']}, {res['stage']}]  ->  {res['verdict']}"]
    order = {"FAIL": 0, "WARN": 1, "LATER": 2, "INFO": 3}
    for f in sorted(res["findings"], key=lambda f: order[f["level"]]):
        lines.append(f"  {f['level']:<5} {f['check']:<17} {f['message']}")
    return "\n".join(lines)


def self_test() -> None:
    assert _mul(_I, (2, 0, 0, 2, 0, 0)) == (2, 0, 0, 2, 0, 0)
    st = {"text": [], "strokes": [], "rgb_fill": set(), "rgb_stroke": set(), "cmyk": False, "do": []}
    _scan_content(b"q 0.25 w 1 0 0 rg 0 0 m 10 10 l S BT /F1 5 Tf (x) Tj ET Q q 100 0 0 50 0 0 cm /I1 Do Q 0 1 0 rg", st)
    assert st["strokes"] == [0.25] and st["text"] == [(5.0, "F1")] and st["do"][0] == ("I1", 100.0, 50.0)
    assert {"red", "green"} <= {_hue(c) for c in st["rgb_fill"]}
    assert [f["level"] for f in _size_findings(174, 120, False)][0] == "INFO"
    assert _size_findings(190, 120, False)[0]["level"] == "FAIL"
    assert _size_findings(100, 100, True)[0]["level"] == "WARN" and _size_findings(101.6, 101.6, True)[0]["level"] == "INFO"
    assert _gray_findings({(0.95, 0.95, 0.95), (0.5, 0.5, 0.5), (0.45, 0.45, 0.45)})
    assert not _gray_findings({(0.9, 0.9, 0.9), (0.6, 0.6, 0.6), (0.2, 0.2, 0.2)})
    print("self-test passed")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check figure files against Cell's production rules.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--stage", choices=("production", "initial"), default="production")
    ap.add_argument("--kind", choices=tuple(DPI), default="colour", help="resolution rule: colour/grayscale 300, bw 500, lineart 1000 dpi")
    ap.add_argument("--ga", action="store_true", help="graphical abstract rules (1200 x 1200 px, 300 dpi, Arial 8-12 pt)")
    ap.add_argument("--width-mm", type=float, help="printed width for raster files without a stored resolution")
    ap.add_argument("--json"); ap.add_argument("--strict", action="store_true"); ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        self_test(); return 0
    if not a.files:
        ap.error("give at least one file")
    results = [audit_file(Path(f), a.kind, a.ga, a.stage, a.width_mm) for f in a.files]
    print("\n\n".join(render(r) for r in results))
    if a.json:
        Path(a.json).write_text(json.dumps(results, indent=1))
    v = {r["verdict"] for r in results}
    if "NOT AUDITABLE" in v:
        return 2
    return 1 if "FIX BEFORE UPLOAD" in v or (a.strict and "REVIEW" in v) else 0


if __name__ == "__main__":
    sys.exit(main())
