#!/usr/bin/env python3
"""Tests for the Cell figure scripts. Run: python3 tests/test_cell_figure.py"""
from __future__ import annotations

import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import cell_style as cs  # noqa: E402
import cell_templates as ct  # noqa: E402
import validate_cell_figure as v  # noqa: E402


def levels(res, check):
    return [f["level"] for f in res["findings"] if f["check"] == check]


def main() -> int:
    v.self_test()
    warnings.simplefilter("ignore")
    cs.use_cell_style(quiet=True)
    tmp = Path(tempfile.mkdtemp(prefix="cellfig_"))

    # 1. sizes and refusals
    assert cs.width_mm("single") == 85 and cs.width_mm("mid") == 114 and cs.width_mm("full") == 174
    for bad in (lambda: cs.width_mm(180), lambda: cs.use_cell_style(base_pt=5), lambda: cs.gray_fills(5)):
        try:
            bad(); raise AssertionError("should have been refused")
        except ValueError:
            pass
    assert len(cs.gray_fills(4)) == 4
    assert cs.red_green_clash(["#D55E00", "#009E73"]) and not cs.red_green_clash(cs.CYCLE)
    assert cs.sub(10) == "₁₀" and cs.sup(-5) == "⁻⁵"

    # 2. demo figure passes every gate and the file audit (apart from the Arial note)
    out = ct.demo(tmp)
    assert out["size_mm"] == [174.0, 112.0], out["size_mm"]
    assert [g["verdict"] for g in out["gates"]][:2] == ["PASS", "PASS"], out["gates"]
    pdf, tif = out["audit"]
    assert "FAIL" not in {f["level"] for f in pdf["findings"]}, pdf
    assert tif["verdict"] == "PASS", tif
    assert levels(pdf, "text size") == ["INFO"] and levels(pdf, "strokes") == ["INFO"]

    # 3. a deliberately bad figure is caught
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 3))                   # 203 mm wide
    ax.plot([0, 1], [0, 1], lw=0.2, color="red"); ax.plot([0, 1], [1, 0], lw=3, color="green")
    ax.set_xlabel("tiny", fontsize=4); ax.set_title("huge", fontsize=14)
    bad = tmp / "bad.pdf"; fig.savefig(bad)
    res = v.audit_file(bad)
    assert res["verdict"] == "FIX BEFORE UPLOAD"
    assert "FAIL" in levels(res, "size") and "FAIL" in levels(res, "text size")
    assert "WARN" in levels(res, "strokes") and "WARN" in levels(res, "colour")
    assert v.audit_file(bad, stage="initial")["verdict"] == "OK FOR FIRST SUBMISSION"
    st = cs.style_report(fig)
    assert st["verdict"] == "REVIEW" and any("red and green" in x for x in st["findings"])

    # 4. gates: misaligned panels and overlapping text block the export
    fig, axes = cs.cell_figure("full", 60, nrows=1, ncols=2)
    fig.set_layout_engine("none")
    axes[1].set_position([0.55, 0.30, 0.4, 0.5])
    assert cs.alignment_report(fig)["verdict"] == "FIX BEFORE DELIVERY"
    fig, ax = cs.cell_figure("single", 50)
    ax.text(0.5, 0.5, "label one"); ax.text(0.5, 0.5, "label two")
    assert cs.overlap_report(fig)["verdict"] == "FIX BEFORE DELIVERY"
    try:
        cs.save_cell(fig, tmp / "blocked"); raise AssertionError("export should be blocked")
    except cs.CellFigureError:
        pass
    assert not (tmp / "blocked.pdf").exists()

    # 5. lowercase panel letters are refused
    try:
        cs.panel_label(ax, "a"); raise AssertionError
    except ValueError:
        pass

    # 6. graphical abstract canvas
    fig, ax = cs.graphical_abstract_canvas()
    ax.text(50, 50, "message", fontsize=10, ha="center")
    ga = tmp / "ga.tiff"; fig.savefig(ga, dpi=300, pil_kwargs={"compression": "tiff_lzw"}); cs._flatten_rgb(ga, 300)
    r = v.audit_file(ga, ga=True)
    assert "FAIL" not in {f["level"] for f in r["findings"]}, r
    fig.savefig(tmp / "ga.pdf")
    r = v.audit_file(tmp / "ga.pdf", ga=True)
    assert levels(r, "size") == ["INFO"], r
    print(f"all tests passed ({tmp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
