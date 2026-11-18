"""One figure kit for every journal profile in journals/.

    import sys; sys.path.insert(0, "<journal-factory>/scripts")
    import journal_style as js

    kit = js.use_journal("nature")            # or "cell", "cancer-cell", "science", ...
    fig, axd = js.mosaic([["A", "A", "B"], ["C", "D", "B"]], width="full", height_mm=120)
    js.templates.bar_points(axd["B"], {"Ctrl": a, "Treated": b}, ylabel="Signal (a.u.)")
    js.label_panels(axd)                      # a, b, c for Nature; A, B, C for Cell
    js.save(fig, "out/Figure 1")              # gates -> files in the journal's formats -> audit

The drawing code, the gates and the file audit are the ones in cell-skills/cell-figure; this
module points them at the chosen journal's widths, type sizes, panel-letter case, stroke range,
resolution and formats. Numbers come from journals/<id>.json and are only as reliable as that
profile's `verified.level` (official / secondary / memory): `use_journal` says which.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HOME / "cell-skills" / "cell-figure" / "scripts"))

import cell_style as _cs            # noqa: E402
import cell_templates as templates  # noqa: E402
import validate_cell_figure as audit  # noqa: E402

CURRENT: dict = {}


def profile(journal: str) -> dict:
    f = HOME / "journals" / f"{journal}.json"
    if not f.is_file():
        known = ", ".join(sorted(p.stem for p in (HOME / "journals").glob("*.json") if not p.name.startswith("_")))
        raise ValueError(f"no profile for '{journal}'. Known: {known}. Create one with: jf adapt \"<journal name>\"")
    return json.loads(f.read_text())


def formats_for(p: dict) -> tuple:
    """File types this kit writes by default: PDF (vector, editable text) plus TIFF when the journal lists it.

    EPS is left out on purpose: it drops transparency and grows large. Pass formats=("eps",) to save() if needed.
    """
    want = [x.split()[0].lower() for x in p["figure"].get("formats", [])]
    return ("pdf", "tiff") if ("tiff" in want or "tif" in want) else ("pdf",)


def use_journal(journal: str, base_pt: float | None = None, quiet: bool = False) -> dict:
    """Configure style, gates and audit for a journal; set matplotlib rcParams. Returns the kit."""
    p = profile(journal)
    _cs.configure(p)
    lvl = p.get("verified", {}).get("level", "memory")
    if lvl != "official" and not quiet:
        warnings.warn(f"{p['name']}: figure numbers are '{lvl}' (not read on the journal's own pages). "
                      "Confirm them before final files.", stacklevel=2)
    st = _cs.use_cell_style(base_pt=base_pt, quiet=quiet)
    CURRENT.clear()
    CURRENT.update({"id": p["id"], "name": p["name"], "verified": lvl, "widths_mm": dict(_cs.CELL["widths_mm"]),
                    "text_pt": _cs.CELL["text_pt"], "stroke_pt": _cs.CELL["stroke_pt"], "panel_letters": _cs.CELL["label_case"],
                    "fonts": _cs.CELL["fonts"], "formats": formats_for(p), **st})
    return dict(CURRENT)


def _need():
    if not CURRENT:
        raise RuntimeError("call use_journal('<id>') first")


def figure(width="full", height_mm: float = 100.0, nrows: int = 1, ncols: int = 1, **kw):
    _need(); return _cs.cell_figure(width, height_mm, nrows, ncols, **kw)


def mosaic(layout, width="full", height_mm: float = 120.0, **kw):
    _need(); return _cs.cell_mosaic(layout, width, height_mm, **kw)


def label_panels(axes, **kw):
    _need(); return _cs.label_panels(axes, **kw)


def save(fig, stem, formats=None, **kw) -> dict:
    """Gates, export in the journal's formats, audit. Raises when a gate fails (strict=False for a draft)."""
    _need(); return _cs.save_cell(fig, stem, formats=formats or CURRENT["formats"], **kw)


def check(path, kind: str = "colour", stage: str = "production", width_mm: float | None = None) -> dict:
    """Audit an exported file against the current journal."""
    _need(); return audit.audit_file(Path(path), kind=kind, stage=stage, width_mm=width_mm)


# the rest of the style helpers work unchanged for every journal
PALETTE, CYCLE = _cs.PALETTE, _cs.CYCLE
sub, sup, scale_bar, image_axes, gray_fills, check_cmap, run_gates = (_cs.sub, _cs.sup, _cs.scale_bar, _cs.image_axes, _cs.gray_fills,
                                                                      _cs.check_cmap, _cs.run_gates)


def demo(journal: str, outdir) -> dict:
    """Six-panel full-width figure from SIMULATED data in the journal's style, with the audit."""
    import matplotlib
    matplotlib.use("Agg")
    k = use_journal(journal, quiet=True)
    real = _cs.use_cell_style
    _cs.use_cell_style = lambda *a, **kw: real(*a, **{**kw, "quiet": True})   # demo() calls it again
    save_real = _cs.save_cell
    _cs.save_cell = lambda fig, stem, formats=None, **kw: save_real(fig, stem, formats=k["formats"], **kw)
    try:
        return templates.demo(outdir)
    finally:
        _cs.use_cell_style, _cs.save_cell = real, save_real


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Figure kit for any journal profile.")
    ap.add_argument("journal"); ap.add_argument("--demo", metavar="OUTDIR"); ap.add_argument("--check", nargs="+", metavar="FILE")
    ap.add_argument("--kind", default="colour"); ap.add_argument("--stage", default="production"); ap.add_argument("--width-mm", type=float)
    a = ap.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        k = use_journal(a.journal, quiet=True)
    print(f"{k['name']} ({k['verified']}): widths {k['widths_mm']} mm; text {k['text_pt'][0]:g}-{k['text_pt'][1]:g} pt; "
          f"panel letters {k['panel_letters']}; strokes {k['stroke_pt'][0]:g}-{k['stroke_pt'][1]:g} pt; formats {', '.join(k['formats'])}")
    rc = 0
    if a.demo:
        r = demo(a.journal, a.demo)
        print("size (mm):", " x ".join(f"{float(x):.1f}" for x in r["size_mm"])); [print(" ", g["check"], "->", g["verdict"], *g["findings"][:3]) for g in r["gates"]]
        for x in r.get("audit", []) if isinstance(r.get("audit"), list) else []:
            print(audit.render(x))
    for f in a.check or []:
        res = check(f, a.kind, a.stage, a.width_mm); print(audit.render(res))
        rc = rc or (1 if res["verdict"] == "FIX BEFORE UPLOAD" else 0)
    sys.exit(rc)
