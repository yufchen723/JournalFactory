#!/usr/bin/env python3
"""Cell (Cell Press) figure style for matplotlib.

Numbers come from cell-shared/journal-formats/cell.md section 5 (read on cell.com
2026-11-18): widths 85 / 114 / 174 mm, recommended maximum 165 x 200 mm, Arial only,
text about 6-8 pt, capital panel letters, strokes 0.5-1.5 pt, RGB, no red with green,
gray fills 10-80% and at least 20% apart, TIFF or PDF, at most 20 MB per figure.

Things Cell does not specify (panel-letter size and weight, palette, tick length) are
house choices; they are marked HOUSE below and can be changed freely.

Use:

    import cell_style as cs
    cs.use_cell_style()
    fig, axes = cs.cell_figure("full", 110, nrows=2, ncols=3)
    ...
    cs.label_panels(axes.ravel())              # A, B, C ...
    cs.save_cell(fig, "Figure 1")               # alignment + overlap gate, PDF + TIFF, audit
"""
from __future__ import annotations

import colorsys
import json
import string
import warnings
from pathlib import Path

MM = 1 / 25.4  # inch per mm

# --- Cell rules (cell.md section 5) -------------------------------------------------
CELL = {
    "widths_mm": {"single": 85.0, "mid": 114.0, "full": 174.0},
    "recommended_max_mm": (165.0, 200.0),
    "font": "Arial",
    "text_pt": (6.0, 8.0),
    "stroke_pt": (0.5, 1.5),
    "dpi": {"colour": 300, "grayscale": 300, "bw": 500, "lineart": 1000},
    "max_file_mb": 20.0,
    "gray_fill": {"lightest": 0.10, "darkest": 0.80, "min_step": 0.20},
    "ga": {"px": 1200, "dpi": 300, "text_pt": (8.0, 12.0)},
    # the four keys below let Journal Factory point this module at another journal (configure())
    "name": "Cell",
    "label_case": "upper",
    "fonts": ["Arial"],
    "rules": {"red_green": True, "gray_fill": True},
}

# --- HOUSE choices (not Cell rules) -----------------------------------------------------
HOUSE = {
    "base_pt": 7.0,       # axis titles, panel titles
    "tick_pt": 6.0,       # tick labels, legend entries
    "label_pt": 8.0,      # panel letters: capital (Cell rule), bold 8 pt (house)
    "axis_lw": 0.5,       # the thinnest stroke Cell allows
    "data_lw": 1.0,
    "marker_pt": 3.0,
}

# Colour-blind-safe categorical palette (Okabe-Ito order adapted so that red and green
# are never both in the first seven colours). "green" is kept out of the default cycle.
PALETTE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "yellow": "#F0E442",
    "gray": "#7F7F7F",
    "black": "#000000",
    "green": "#009E73",   # do not combine with vermilion in one figure (Cell: no red with green)
}
CYCLE = [PALETTE[k] for k in ("blue", "orange", "sky", "vermilion", "purple", "yellow", "gray")]
SEQUENTIAL = "viridis"      # perceptually uniform, no red
DIVERGING = "RdBu_r"        # blue-white-red, centred at 0
FORBIDDEN_CMAPS = ("jet", "rainbow", "hsv", "gist_rainbow", "nipy_spectral", "RdYlGn", "RdYlGn_r", "PiYG", "PRGn")

FALLBACK_FONTS = ["Arial", "Liberation Sans", "Helvetica", "Nimbus Sans", "DejaVu Sans"]


def load_profile(path: str | Path | None = None) -> dict:
    """Overlay journals/cell.json (Journal Factory) on the built-in numbers, if found."""
    cand = [Path(path)] if path else []
    here = Path(__file__).resolve()
    cand += [p / "journals" / "cell.json" for p in here.parents[:5]]
    for c in cand:
        if c.is_file():
            try:
                F = json.loads(c.read_text())["figure"]
                CELL["widths_mm"].update({{"double": "full"}.get(k, k): float(v) for k, v in F["widths_mm"].items()})
                CELL["text_pt"] = (float(F["font_pt"]["min"]), float(F["font_pt"]["max"]))
                CELL["stroke_pt"] = (float(F["line_pt"]["min"]), float(F["line_pt"]["max"]))
                CELL["max_file_mb"] = float(F.get("max_file_mb", CELL["max_file_mb"]))
            except Exception as exc:  # profile problems never block plotting
                warnings.warn(f"cell.json not used ({exc})")
            break
    return CELL


def configure(profile: dict) -> dict:
    """Point this module (and the file audit) at another journal's profile (journals/<id>.json).

    Used by Journal Factory's scripts/journal_style.py. Cell stays the default; nothing here
    runs unless it is called. Values a profile does not state keep their current value.
    """
    F = profile["figure"]
    W = {k: float(v) for k, v in F["widths_mm"].items()}
    full = W.get("double") or max(W.values())
    CELL["widths_mm"] = {"single": W.get("single", min(W.values())), "full": full}
    if "mid" in W:
        CELL["widths_mm"]["mid"] = W["mid"]
    CELL["text_pt"] = (float(F["font_pt"]["min"]), float(F["font_pt"]["max"]))
    CELL["stroke_pt"] = (float(F["line_pt"]["min"]), float(F["line_pt"]["max"]))
    d = F.get("dpi", {})
    photo = int(d.get("photo", 300)); line = int(d.get("line_art", 600))
    CELL["dpi"] = {"colour": photo, "grayscale": photo, "bw": int(d.get("black_white", line)), "lineart": line}
    CELL["max_file_mb"] = float(F.get("max_file_mb", 1e9))   # 1e9 = the profile states no limit
    rec = F.get("recommended_max_mm")
    CELL["recommended_max_mm"] = (float(rec[0]), float(rec[1])) if rec else (full, float(F.get("max_height_mm", 247)))
    CELL["name"] = profile.get("name", profile.get("id", "journal"))
    CELL["label_case"] = F.get("panel_label", {}).get("case", "upper")
    CELL["fonts"] = list(F.get("font_family") or ["Arial"])
    CELL["rules"] = {"red_green": True, "gray_fill": "gray_fill" in F}
    lo, hi = CELL["text_pt"]
    HOUSE["base_pt"] = min(max(7.0, lo), hi)
    HOUSE["tick_pt"] = min(max(6.0, lo), HOUSE["base_pt"])
    HOUSE["label_pt"] = float(F.get("panel_label", {}).get("pt", 8))
    slo, shi = CELL["stroke_pt"]
    HOUSE["axis_lw"] = min(max(0.5, slo), shi)
    HOUSE["data_lw"] = min(max(1.0, slo), shi)
    try:
        import validate_cell_figure as v
        v.configure(profile)
    except ImportError:
        pass
    return CELL


def arial_available() -> bool:
    from matplotlib import font_manager as fm
    return any(f.name == "Arial" for f in fm.fontManager.ttflist)


def use_cell_style(base_pt: float | None = None, quiet: bool = False) -> dict:
    """Set matplotlib rcParams for a Cell figure. Returns the values used."""
    import matplotlib as mpl

    base = float(base_pt or HOUSE["base_pt"])
    lo, hi = CELL["text_pt"]
    if not lo <= base <= hi:
        raise ValueError(f"base_pt {base} is outside {CELL['name']}'s {lo:g}-{hi:g} pt")
    tick = max(lo, min(base, HOUSE["tick_pt"]))
    if not arial_available() and not quiet:
        warnings.warn(
            "Arial is not installed: the figure is drawn in a metric-compatible fallback "
            f"(Liberation Sans). {CELL['name']} asks for {' or '.join(CELL['fonts'])}; re-export on a machine with Arial "
            "before the production upload.", stacklevel=2)
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": FALLBACK_FONTS,
        "font.size": base,
        "axes.titlesize": base, "axes.labelsize": base,
        "xtick.labelsize": tick, "ytick.labelsize": tick,
        "legend.fontsize": tick, "legend.title_fontsize": tick,
        "figure.titlesize": base,
        "mathtext.fontset": "custom", "mathtext.rm": "sans", "mathtext.it": "sans:italic",
        "mathtext.bf": "sans:bold", "mathtext.cal": "sans", "mathtext.tt": "sans", "mathtext.sf": "sans",
        "mathtext.default": "regular",
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",   # text stays text, fonts embedded
        "axes.linewidth": HOUSE["axis_lw"],
        "xtick.major.width": HOUSE["axis_lw"], "ytick.major.width": HOUSE["axis_lw"],
        "xtick.minor.width": HOUSE["axis_lw"], "ytick.minor.width": HOUSE["axis_lw"],
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.minor.size": 1.5, "ytick.minor.size": 1.5,
        "xtick.major.pad": 2, "ytick.major.pad": 2, "axes.labelpad": 2, "axes.titlepad": 3,
        "lines.linewidth": HOUSE["data_lw"], "lines.markersize": HOUSE["marker_pt"],
        "patch.linewidth": HOUSE["axis_lw"], "hatch.linewidth": HOUSE["axis_lw"],
        "grid.linewidth": HOUSE["axis_lw"], "boxplot.flierprops.markersize": 2,
        "errorbar.capsize": 1.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=CYCLE),
        "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white",
        "legend.frameon": False, "legend.handlelength": 1.2, "legend.borderaxespad": 0.3,
        "image.cmap": SEQUENTIAL,
        "figure.dpi": 150, "savefig.dpi": CELL["dpi"]["colour"],
        "figure.constrained_layout.use": True,
        "figure.constrained_layout.h_pad": 2 / 72, "figure.constrained_layout.w_pad": 2 / 72,
        "figure.constrained_layout.hspace": 0.04, "figure.constrained_layout.wspace": 0.04,
    })
    return {"base_pt": base, "tick_pt": tick, "arial": arial_available()}


def width_mm(width: str | float) -> float:
    if isinstance(width, str):
        key = {"1": "single", "1.5": "mid", "2": "full", "double": "full", "one": "single"}.get(width, width)
        return CELL["widths_mm"][key]
    w = float(width)
    if w > CELL["widths_mm"]["full"] + 1e-6:
        raise ValueError(f"width {w} mm is wider than {CELL['name']}'s full page width ({CELL['widths_mm']['full']} mm)")
    return w


def cell_figure(width: str | float = "full", height_mm: float = 100.0, nrows: int = 1, ncols: int = 1, **kw):
    """A figure at an exact Cell width. Returns (fig, axes) like plt.subplots.

    width: "single" (85 mm), "mid" (114 mm), "full" (174 mm) or a number in mm (<= 174).
    """
    import matplotlib.pyplot as plt

    w = width_mm(width)
    rec_w, rec_h = CELL["recommended_max_mm"]
    if height_mm > rec_h:
        warnings.warn(f"height {height_mm:g} mm is above {CELL['name']}'s recommended {rec_h:g} mm; the legend may not fit under the figure", stacklevel=2)
    if w > rec_w:
        # full width (174) is allowed; 165 is the recommendation that leaves room for margins
        pass
    fig, axes = plt.subplots(nrows, ncols, figsize=(w * MM, height_mm * MM), **kw)
    fig._cell_size_mm = (w, float(height_mm))
    return fig, axes


def cell_mosaic(layout, width: str | float = "full", height_mm: float = 120.0, **kw):
    """Asymmetric layouts: cell_mosaic([["A", "A", "B"], ["C", "D", "B"]]). Keys become panel letters."""
    import matplotlib.pyplot as plt

    w = width_mm(width)
    fig, axd = plt.subplot_mosaic(layout, figsize=(w * MM, height_mm * MM), **kw)
    fig._cell_size_mm = (w, float(height_mm))
    return fig, axd


def panel_label(ax, letter: str, dx_pt: float = -22.0, dy_pt: float = 4.0, size: float | None = None):
    """Capital bold panel letter at a fixed offset (points) from the axes' top-left corner."""
    from matplotlib.transforms import ScaledTranslation

    letter = str(letter)
    if CELL["label_case"] == "upper" and not letter.isupper():
        raise ValueError(f"{CELL['name']} panel labels are capital letters (got {letter!r})")
    if CELL["label_case"] == "lower":
        letter = letter.lower()
    fig = ax.figure
    tr = ax.transAxes + ScaledTranslation(dx_pt / 72, dy_pt / 72, fig.dpi_scale_trans)
    t = ax.text(0, 1, letter, transform=tr, fontsize=size or HOUSE["label_pt"], fontweight="bold",
                va="bottom", ha="left", clip_on=False)
    t.set_gid(f"panel-label-{letter}")
    t.set_in_layout(True)
    return t


def label_panels(axes, letters: str | None = None, **kw):
    """Label axes in reading order with A, B, C ... (pass a dict from cell_mosaic to use its keys)."""
    if isinstance(axes, dict):
        return {k: panel_label(ax, k, **kw) for k, ax in axes.items() if str(k).isalpha() and (str(k).isupper() or CELL["label_case"] == "lower")}
    letters = letters or (string.ascii_lowercase if CELL["label_case"] == "lower" else string.ascii_uppercase)
    return [panel_label(ax, letters[i], **kw) for i, ax in enumerate(axes)]


_SUB = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")
_SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def sub(x) -> str:
    """Subscript as real characters (log₂, CO₂). Mathtext subscripts are drawn at 70% size,
    which puts a 7 pt label's subscript at 4.9 pt, below Cell's 6 pt."""
    return str(x).translate(_SUB)


def sup(x) -> str:
    """Superscript as real characters (10⁻⁵, mm²)."""
    return str(x).translate(_SUP)


def gray_fills(n: int) -> list[str]:
    """n gray fills that follow Cell's rule: between 10% and 80% black, at least 20% apart."""
    g = CELL["gray_fill"]
    most = int((g["darkest"] - g["lightest"]) / g["min_step"] + 1e-9) + 1
    if n > most:
        raise ValueError(f"Cell's gray rule allows at most {most} distinguishable gray fills; use hatching or colour for {n} groups")
    step = (g["darkest"] - g["lightest"]) / max(n - 1, 1) if n > 1 else 0
    blacks = [g["lightest"] + i * step for i in range(n)] if n > 1 else [0.45]
    return ["#" + f"{int(round(255 * (1 - b))):02x}" * 3 for b in blacks]


def _hue_class(color) -> str | None:
    from matplotlib.colors import to_rgb
    r, g, b = to_rgb(color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.35 or v < 0.25:
        return None
    deg = h * 360
    if deg < 30 or deg >= 340:
        return "red"
    if 80 <= deg < 170:
        return "green"
    return None


def red_green_clash(colors) -> bool:
    """True when the colour set holds both a red and a green (Cell: do not use them together)."""
    kinds = {_hue_class(c) for c in colors}
    return {"red", "green"} <= kinds


def check_cmap(name: str) -> str:
    base = name
    if base in FORBIDDEN_CMAPS:
        raise ValueError(f"colormap {name!r} is not suitable (rainbow or red-green); use {SEQUENTIAL!r} or {DIVERGING!r}")
    return name


def scale_bar(ax, length: float, label: str, loc: str = "lower right", lw: float = 1.0, color: str = "black"):
    """Scale bar of `length` data units. Cell requires one on every microscopy or tissue image."""
    from matplotlib.font_manager import FontProperties
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    ax.figure.canvas.draw()
    pt_per_unit = abs(ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]) * 72 / ax.figure.dpi
    lw = min(max(lw, CELL["stroke_pt"][0]), CELL["stroke_pt"][1])
    bar = AnchoredSizeBar(ax.transData, length, label, loc, frameon=False, color=color, pad=0.2, sep=2,
                          size_vertical=lw / max(pt_per_unit, 1e-9), fontproperties=FontProperties(size=HOUSE["tick_pt"]))
    ax.add_artist(bar)
    return bar


def image_axes(ax):
    """An axes for a tissue image or spatial map: no frame, equal aspect."""
    ax.set_aspect("equal", adjustable="datalim")   # the frame keeps its grid cell; the data limits adapt
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return ax


# --- gates ------------------------------------------------------------------------------

def _visible_texts(fig):
    """Text that is actually drawn: skips empty strings and tick labels outside the view."""
    from matplotlib.text import Text
    hidden = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            pad = 1e-9 * max(abs(lo), abs(hi), 1)
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not (lo - pad <= tick.get_loc() <= hi + pad):
                    hidden.update((id(tick.label1), id(tick.label2)))
    out = []
    for t in fig.findobj(Text):
        if id(t) in hidden or not t.get_visible() or not t.get_text().strip():
            continue
        ax = getattr(t, "axes", None)
        if ax is not None and not ax.get_visible():
            continue
        out.append(t)
    return out


def _data_axes(fig):
    return [a for a in fig.axes if a.get_visible() and not str(a.get_label()).startswith("<colorbar") and a.get_gid() != "cell-aux"]


def alignment_report(fig, tol_pt: float = 1.5) -> dict:
    """Edges of panels that sit in the same grid row or column must agree within tol_pt.

    Same idea as the nature-figure alignment gate: measure the final axes rectangles, in
    points, after the layout is drawn. Mark an axes as exempt with ax.set_gid("cell-aux").
    """
    fig.canvas.draw()
    W, H = (v * 72 for v in fig.get_size_inches())
    rows: dict = {}; cols: dict = {}; exempt: list = []
    boxes = {}
    for i, ax in enumerate(_data_axes(fig)):
        p = ax.get_position()
        boxes[i] = (p.x0 * W, p.y0 * H, p.x1 * W, p.y1 * H)
        try:
            ss = ax.get_subplotspec()
        except AttributeError:
            ss = None
        if ss is None:
            continue
        if ax.get_aspect() != "auto" and ax.get_adjustable() == "box":
            exempt.append(i)        # fixed-aspect image panel: its frame cannot follow the grid
            continue
        gs = id(ss.get_gridspec())
        rows.setdefault((gs, ss.rowspan.start, ss.rowspan.stop), []).append(i)
        cols.setdefault((gs, ss.colspan.start, ss.colspan.stop), []).append(i)
    findings = []
    for key, idx in rows.items():
        if len(idx) < 2:
            continue
        for name, j in (("bottom edge", 1), ("top edge", 3)):
            vals = [boxes[i][j] for i in idx]
            if max(vals) - min(vals) > tol_pt:
                findings.append(f"row {key[1]}: {name} differs by {max(vals) - min(vals):.1f} pt across {len(idx)} panels")
    for key, idx in cols.items():
        if len(idx) < 2:
            continue
        for name, j in (("left edge", 0), ("right edge", 2)):
            vals = [boxes[i][j] for i in idx]
            if max(vals) - min(vals) > tol_pt:
                findings.append(f"column {key[1]}: {name} differs by {max(vals) - min(vals):.1f} pt across {len(idx)} panels")
    n = len(boxes)
    verdict = "NOT APPLICABLE" if n < 2 else ("FIX BEFORE DELIVERY" if findings else "PASS")
    return {"check": "panel alignment", "panels": n, "tolerance_pt": tol_pt, "verdict": verdict, "findings": findings,
            "exempt_fixed_aspect_panels": len(exempt)}


def overlap_report(fig, pad_pt: float = 0.5) -> dict:
    """Text that collides with other text, or runs off the page (rendered boxes, in points)."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    scale = 72 / fig.dpi
    W, H = (v * 72 for v in fig.get_size_inches())
    items = []
    for t in _visible_texts(fig):
        s = t.get_text().strip()
        try:
            b = t.get_window_extent(r)
        except Exception:
            continue
        if b.width <= 0 or b.height <= 0:
            continue
        items.append((s, b.x0 * scale, b.y0 * scale, b.x1 * scale, b.y1 * scale, t))
    findings = []
    for s, x0, y0, x1, y1, t in items:
        if x0 < -pad_pt or y0 < -pad_pt or x1 > W + pad_pt or y1 > H + pad_pt:
            findings.append(f"text {s[:30]!r} runs off the page")
    for i in range(len(items)):
        a = items[i]
        for j in range(i + 1, len(items)):
            b = items[j]
            if a[5] is b[5]:
                continue
            ox = min(a[3], b[3]) - max(a[1], b[1]) - pad_pt
            oy = min(a[4], b[4]) - max(a[2], b[2]) - pad_pt
            if ox > 0 and oy > 0:
                small = min((a[3] - a[1]) * (a[4] - a[2]), (b[3] - b[1]) * (b[4] - b[2]))
                if ox * oy > 0.08 * small:
                    findings.append(f"text {a[0][:24]!r} overlaps {b[0][:24]!r}")
    return {"check": "text overlap", "texts": len(items), "verdict": "FIX BEFORE DELIVERY" if findings else "PASS", "findings": findings[:40]}


def style_report(fig) -> dict:
    """Font sizes, stroke widths, panel letters and colours of the live figure against Cell's rules."""
    from matplotlib.lines import Line2D
    from matplotlib.text import Text
    lo, hi = CELL["text_pt"]; slo, shi = CELL["stroke_pt"]
    findings = []
    texts = _visible_texts(fig)
    small = sorted({round(t.get_fontsize(), 2) for t in texts if t.get_fontsize() < lo - 0.01})
    big = sorted({round(t.get_fontsize(), 2) for t in texts if t.get_fontsize() > hi + 0.01
                  and not str(t.get_gid() or "").startswith("panel-label-")})   # panel letters have their own size rule
    if small:
        findings.append(f"text below {lo:g} pt: {small}")
    if big:
        findings.append(f"text above {hi:g} pt: {big}")
    if any("$" in t.get_text() and ("^" in t.get_text() or "_" in t.get_text()) for t in texts):
        findings.append("mathtext superscripts/subscripts render at 70% of the parent size and can fall below 6 pt; check the PDF audit")
    thin = sorted({round(l.get_linewidth(), 2) for l in fig.findobj(Line2D) if l.get_visible() and l.get_linestyle() not in ("None", "", " ") and 0 < l.get_linewidth() < slo - 0.01})
    thick = sorted({round(l.get_linewidth(), 2) for l in fig.findobj(Line2D) if l.get_visible() and l.get_linestyle() not in ("None", "", " ") and l.get_linewidth() > shi + 0.01})
    if thin:
        findings.append(f"strokes below {slo:g} pt: {thin}")
    if thick:
        findings.append(f"strokes above {shi:g} pt: {thick}")
    labels = [t.get_text() for t in fig.findobj(Text) if str(t.get_gid() or "").startswith("panel-label-")]
    if len(_data_axes(fig)) > 1 and not labels:
        findings.append("multi-panel figure without panel letters (use label_panels)")
    if labels and sorted(x.upper() for x in labels) != list(string.ascii_uppercase[:len(labels)]):
        findings.append(f"panel letters are not a continuous A.. sequence: {sorted(labels)}")
    cols = set()
    for ax in fig.axes:
        for l in ax.lines:
            cols.add(l.get_color()) if isinstance(l.get_color(), str) else None
        for p in ax.patches:
            try:
                fc = p.get_facecolor()
                if fc[3] > 0.2:
                    cols.add(tuple(fc[:3]))
            except Exception:
                pass
    try:
        if red_green_clash(cols):
            findings.append("red and green are used together (" + ("Cell: avoid" if CELL["name"] == "Cell" else "hard for colour-blind readers") + "); change one of them")
    except Exception:
        pass
    return {"check": f"{CELL['name']} style", "verdict": "REVIEW" if findings else "PASS", "findings": findings}


def run_gates(fig, tol_pt: float = 1.5) -> list[dict]:
    return [alignment_report(fig, tol_pt), overlap_report(fig), style_report(fig)]


class CellFigureError(RuntimeError):
    pass


def save_cell(fig, stem: str | Path, formats=("pdf", "tiff"), kind: str = "colour", dpi: int | None = None,
              strict: bool = True, preview: bool = True, audit: bool = True) -> dict:
    """Run the gates, then write production files at the exact figure size.

    formats: any of pdf, tiff, png, svg, eps, jpg (Cell prefers TIFF and PDF).
    kind: "colour"/"grayscale" (>= 300 dpi), "bw" (>= 500), "lineart" (>= 1000).
    strict: raise CellFigureError when alignment or text overlap fails.
    No bbox_inches="tight": that would change the physical width.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    need = CELL["dpi"][kind]
    dpi = int(dpi or need)
    if dpi < need:
        raise ValueError(f"{kind} figures need at least {need} dpi (got {dpi})")
    gates = run_gates(fig)
    blocking = [g for g in gates if g["verdict"] == "FIX BEFORE DELIVERY"]
    out = {"stem": str(stem), "size_mm": [round(v * 25.4, 2) for v in fig.get_size_inches()], "gates": gates, "files": []}
    (stem.parent / f"{stem.name}.qa.json").write_text(json.dumps(out, indent=1))
    if blocking and strict:
        msg = "; ".join(f"{g['check']}: " + " | ".join(g["findings"][:4]) for g in blocking)
        raise CellFigureError(f"figure not saved ({msg}). Fix the layout, or pass strict=False to export a draft.")
    for fmt in formats:
        f = stem.parent / f"{stem.name}.{fmt}"
        if fmt in ("tiff", "tif"):
            fig.savefig(f, dpi=dpi, pil_kwargs={"compression": "tiff_lzw"})
            _flatten_rgb(f, dpi)
        elif fmt in ("png", "jpg", "jpeg"):
            fig.savefig(f, dpi=dpi)
            _flatten_rgb(f, dpi)
        else:
            fig.savefig(f, dpi=max(600, dpi))   # dpi here only sets the resolution of rasterised layers
        mb = f.stat().st_size / 1e6
        if mb > CELL["max_file_mb"]:
            warnings.warn(f"{f.name} is {mb:.1f} MB; {CELL['name']}'s limit is {CELL['max_file_mb']:g} MB per figure")
        out["files"].append({"path": str(f), "mb": round(mb, 2)})
    if preview and not any(str(x["path"]).endswith(".png") for x in out["files"]):
        p = stem.parent / f"{stem.name}.preview.png"
        fig.savefig(p, dpi=200)
        out["preview"] = str(p)
    if audit:
        try:
            import validate_cell_figure as v
            out["audit"] = [v.audit_file(Path(x["path"]), kind=kind) for x in out["files"]]
        except ImportError:
            out["audit"] = "validate_cell_figure.py not importable; run it on the exported files"
    (stem.parent / f"{stem.name}.qa.json").write_text(json.dumps(out, indent=1, default=str))
    return out


def _flatten_rgb(path: Path, dpi: int) -> None:
    """Cell wants RGB and one layer: drop the alpha channel onto white."""
    try:
        from PIL import Image
    except ImportError:
        return
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        kw = {"dpi": (dpi, dpi)}
        if path.suffix.lower() in (".tif", ".tiff"):
            kw["compression"] = "tiff_lzw"
        bg.save(path, **kw)


def graphical_abstract_canvas():
    """A square canvas for the Cell graphical abstract: 1200 x 1200 px at 300 dpi (4 x 4 in), Arial 8-12 pt."""
    import matplotlib.pyplot as plt
    ga = CELL["ga"]
    side = ga["px"] / ga["dpi"]
    fig = plt.figure(figsize=(side, side), layout="none")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    fig._cell_ga = True
    return fig, ax


load_profile()

if __name__ == "__main__":
    print(json.dumps({"cell": CELL, "house": HOUSE, "arial_installed": arial_available()}, indent=1))
