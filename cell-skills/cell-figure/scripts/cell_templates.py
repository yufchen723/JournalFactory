#!/usr/bin/env python3
"""Panel templates in Cell style. Each function draws into an axes you pass in.

Every template follows the same rules:
- individual data points are drawn next to any mean or box (Cell recommends it);
- error bars and n are returned as text for the legend, never printed on every bar;
- large point clouds are rasterised inside the vector file (>= 600 dpi) so the PDF stays small;
- colours come from cell_style (no red with green, no rainbow maps).

    python cell_templates.py --demo OUTDIR      # builds a demo figure from SIMULATED data
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cell_style as cs  # noqa: E402

RASTER_DPI = 600


def _colorbar(ax, mappable, label="", width=0.03, height=0.6):
    """Slim colour bar in its own inset just right of the panel, so the panel keeps its grid cell."""
    cax = ax.inset_axes([1.02, (1 - height) / 2, width, height])
    cax.set_gid("cell-aux")
    cb = ax.figure.colorbar(mappable, cax=cax)
    cb.set_label(label); cb.outline.set_linewidth(0.5); cb.ax.tick_params(width=0.5, length=2)
    return cb


def bar_points(ax, groups: dict, colors=None, ylabel="", error="sem", seed=0):
    """Mean bar + every data point + error bar. groups: {name: values (one per biological replicate)}.
    Returns the sentence for the legend."""
    rng = np.random.default_rng(seed)
    names = list(groups)
    colors = colors or cs.CYCLE
    for i, k in enumerate(names):
        v = np.asarray(groups[k], float)
        m = v.mean()
        e = v.std(ddof=1) / np.sqrt(len(v)) if error == "sem" else v.std(ddof=1)
        ax.bar(i, m, width=0.62, color=colors[i % len(colors)], alpha=0.55, edgecolor="black", linewidth=0.5, zorder=1)
        ax.errorbar(i, m, yerr=e, color="black", lw=0.75, capsize=1.5, capthick=0.75, zorder=3)
        ax.scatter(i + rng.uniform(-0.16, 0.16, len(v)), v, s=6, color="black", linewidths=0, zorder=4)
    ax.set_xticks(range(len(names)), names)
    ax.set_ylabel(ylabel)
    ax.set_xlim(-0.6, len(names) - 0.4)
    ns = ", ".join(f"{k} n = {len(groups[k])}" for k in names)
    return f"Bars show mean ± {'SEM' if error == 'sem' else 'SD'}; dots are individual replicates ({ns})."


def box_points(ax, groups: dict, colors=None, ylabel="", seed=0, max_points=400):
    """Box (median, quartiles, 1.5 IQR whiskers) + points."""
    rng = np.random.default_rng(seed)
    names = list(groups)
    colors = colors or cs.CYCLE
    data = [np.asarray(groups[k], float) for k in names]
    bp = ax.boxplot(data, positions=range(len(names)), widths=0.55, patch_artist=True, showfliers=False,
                    medianprops=dict(color="black", lw=1.0), boxprops=dict(lw=0.5), whiskerprops=dict(lw=0.5), capprops=dict(lw=0.5))
    for i, b in enumerate(bp["boxes"]):
        b.set_facecolor(colors[i % len(colors)]); b.set_alpha(0.55)
    for i, v in enumerate(data):
        if len(v) > max_points:
            v = rng.choice(v, max_points, replace=False)   # display only; state it in the legend
        ax.scatter(i + rng.uniform(-0.18, 0.18, len(v)), v, s=3, color="black", alpha=0.6, linewidths=0, zorder=3,
                   rasterized=len(v) > 200)
    ax.set_xticks(range(len(names)), names)
    ax.set_ylabel(ylabel)
    return "Boxes show median and quartiles; whiskers extend to 1.5 × the interquartile range; dots are individual values."


def paired_lines(ax, before, after, labels=("Before", "After"), ylabel="", color=None):
    """Paired design: one line per subject. Use when the effect is within subject."""
    before = np.asarray(before, float); after = np.asarray(after, float)
    for b, a in zip(before, after):
        ax.plot([0, 1], [b, a], color=cs.PALETTE["gray"], lw=0.5, zorder=1)
    ax.scatter(np.zeros_like(before), before, s=8, color=color or cs.PALETTE["blue"], zorder=2, linewidths=0)
    ax.scatter(np.ones_like(after), after, s=8, color=color or cs.PALETTE["vermilion"], zorder=2, linewidths=0)
    ax.set_xticks([0, 1], labels); ax.set_xlim(-0.4, 1.4); ax.set_ylabel(ylabel)
    return f"Lines join paired measurements (n = {len(before)} pairs)."


def volcano(ax, log2fc, padj, labels=None, fc_cut=1.0, p_cut=0.05, top=8, xlabel="log" + cs.sub(2) + " fold change"):
    """Volcano with rasterised points and direct labels for the top hits."""
    log2fc = np.asarray(log2fc, float); y = -np.log10(np.clip(np.asarray(padj, float), 1e-300, 1))
    up = (log2fc >= fc_cut) & (padj < p_cut); down = (log2fc <= -fc_cut) & (padj < p_cut); ns = ~(up | down)
    ax.scatter(log2fc[ns], y[ns], s=2, color="#B3B3B3", linewidths=0, rasterized=True)
    ax.scatter(log2fc[down], y[down], s=3, color=cs.PALETTE["blue"], linewidths=0, rasterized=True)
    ax.scatter(log2fc[up], y[up], s=3, color=cs.PALETTE["vermilion"], linewidths=0, rasterized=True)
    ax.axhline(-np.log10(p_cut), color="black", lw=0.5, ls=(0, (3, 3)))
    for x in (-fc_cut, fc_cut):
        ax.axvline(x, color="black", lw=0.5, ls=(0, (3, 3)))
    if labels is not None:
        score = np.where(ns, -1, np.abs(log2fc) * y)
        for i in np.argsort(score)[::-1][:top]:
            if score[i] <= 0:
                break
            ax.annotate(str(labels[i]), (log2fc[i], y[i]), xytext=(3 if log2fc[i] > 0 else -3, 2), textcoords="offset points",
                        fontsize=cs.HOUSE["tick_pt"], fontstyle="italic", ha="left" if log2fc[i] > 0 else "right", va="bottom")
    ax.set_xlabel(xlabel); ax.set_ylabel("−log" + cs.sub(10) + " adjusted p")
    ax.set_ylim(0, y.max() * 1.12); ax.margins(x=0.12)
    return f"{int(up.sum())} up and {int(down.sum())} down (|log2 fold change| ≥ {fc_cut:g}, adjusted p < {p_cut:g})."


def heatmap(ax, matrix, row_labels=None, col_labels=None, center=None, cbar_label="", cmap=None, italic_rows=False):
    """Heatmap with a slim colour bar. center=0 switches to the diverging map."""
    M = np.asarray(matrix, float)
    cmap = cs.check_cmap(cmap or (cs.DIVERGING if center is not None else cs.SEQUENTIAL))
    kw = {}
    if center is not None:
        lim = np.nanmax(np.abs(M - center)); kw = dict(vmin=center - lim, vmax=center + lim)
    im = ax.imshow(M, aspect="auto", cmap=cmap, interpolation="nearest", **kw)
    if col_labels is not None:
        ax.set_xticks(range(M.shape[1]), col_labels, rotation=45, ha="right", rotation_mode="anchor")
    if row_labels is not None:
        ax.set_yticks(range(M.shape[0]), row_labels, fontstyle="italic" if italic_rows else "normal")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    _colorbar(ax, im, cbar_label)
    return im


def dot_plot(ax, frac, mean, row_labels, col_labels, size_max=42, cbar_label="Mean expression (scaled)", italic_cols=True):
    """Marker dot plot: size = fraction of cells or pixels expressing, colour = mean expression."""
    frac = np.asarray(frac, float); mean = np.asarray(mean, float)
    yy, xx = np.mgrid[0:frac.shape[0], 0:frac.shape[1]]
    sc = ax.scatter(xx, yy, s=frac * size_max, c=mean, cmap=cs.SEQUENTIAL, edgecolors="black", linewidths=0.25)
    ax.set_xticks(range(frac.shape[1]), col_labels, rotation=45, ha="right", rotation_mode="anchor",
                  fontstyle="italic" if italic_cols else "normal")
    ax.set_yticks(range(frac.shape[0]), row_labels)
    ax.set_xlim(-0.6, frac.shape[1] - 0.4); ax.set_ylim(frac.shape[0] - 0.4, -0.6)
    _colorbar(ax, sc, cbar_label)
    for f in (0.25, 0.5, 1.0):
        ax.scatter([], [], s=f * size_max, color="#B3B3B3", edgecolors="black", linewidths=0.25, label=f"{int(f * 100)}%")
    ax.legend(title="Fraction", loc="upper left", bbox_to_anchor=(1.2, 1.0), labelspacing=0.6)
    return sc


def stacked_composition(ax, table, row_labels, part_labels, colors=None, xlabel="Fraction"):
    """Horizontal stacked bars (composition per sample or group). table: rows x parts, rows sum to 1."""
    T = np.asarray(table, float)
    colors = colors or cs.CYCLE
    left = np.zeros(T.shape[0])
    for j in range(T.shape[1]):
        ax.barh(range(T.shape[0]), T[:, j], left=left, color=colors[j % len(colors)], edgecolor="white", linewidth=0.5,
                height=0.75, label=part_labels[j])
        left += T[:, j]
    ax.set_yticks(range(T.shape[0]), row_labels); ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel(xlabel)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), ncol=1)


def spatial_map(ax, x, y, values=None, categories=None, colors=None, pixel_um=None, bar_um=None, s=0.6,
                cbar_label="", cmap=None, title=None):
    """Tissue map of spots or pixels. Rasterised; equal aspect; scale bar (required by Cell on tissue images).

    values: continuous (colour bar) or categories + colors (dict label -> colour).
    pixel_um: micrometres per coordinate unit; bar_um: scale-bar length in micrometres.
    """
    x = np.asarray(x, float); y = np.asarray(y, float)
    cs.image_axes(ax)
    out = None
    if categories is not None:
        categories = np.asarray(categories)
        labs = list(colors) if colors else list(dict.fromkeys(categories.tolist()))
        colors = colors or {k: cs.CYCLE[i % len(cs.CYCLE)] for i, k in enumerate(labs)}
        for k in labs:
            m = categories == k
            ax.scatter(x[m], y[m], s=s, color=colors[k], linewidths=0, marker="s", rasterized=True)
            ax.scatter([], [], s=10, color=colors[k], marker="s", label=str(k))
        ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), handletextpad=0.2)
    else:
        out = ax.scatter(x, y, s=s, c=values, cmap=cs.check_cmap(cmap or cs.SEQUENTIAL), linewidths=0, marker="s", rasterized=True)
        _colorbar(ax, out, cbar_label)
    ax.invert_yaxis()
    if pixel_um and bar_um:
        ax._cell_scale_bar = (bar_um / pixel_um, f"{bar_um / 1000:g} mm" if bar_um >= 1000 else f"{bar_um:g} µm")
        cs.scale_bar(ax, *ax._cell_scale_bar)
    if title:
        ax.set_title(title)
    return out


def demo(outdir: str | Path, strict: bool = True) -> dict:
    """A six-panel full-width figure from SIMULATED data. For testing the style only."""
    import matplotlib
    matplotlib.use("Agg")
    cs.use_cell_style(quiet=True)
    matplotlib.rcParams["savefig.dpi"] = 300
    matplotlib.rcParams["figure.dpi"] = 100
    rng = np.random.default_rng(7)
    fig, axd = cs.cell_mosaic([["A", "A", "B", "C"], ["D", "D", "E", "F"]], "full", 112)
    for a in axd.values():
        a.figure.dpi = 100

    # A: spatial map, categorical
    n = 9000
    xx = rng.uniform(0, 500, n); yy = rng.uniform(0, 380, n)
    keep = ((xx - 250) / 240) ** 2 + ((yy - 190) / 180) ** 2 < 1
    xx, yy = xx[keep], yy[keep]
    r = np.hypot(xx - 250, yy - 190)
    cat = np.where(r < 60, "Region 1", np.where(r < 130, "Region 2", "Region 3"))
    spatial_map(axd["A"], xx, yy, categories=cat, colors={"Region 1": cs.PALETTE["vermilion"], "Region 2": cs.PALETTE["orange"], "Region 3": cs.PALETTE["sky"]},
                pixel_um=10, bar_um=1000, s=1.2)
    # B: bars with points
    leg_b = bar_points(axd["B"], {"Ctrl": rng.normal(1, 0.15, 6), "Treat 1": rng.normal(1.6, 0.2, 6), "Treat 2": rng.normal(2.1, 0.25, 6)}, ylabel="Relative signal")
    # C: paired
    b = rng.normal(1, 0.2, 10); paired_lines(axd["C"], b, b + rng.normal(0.5, 0.15, 10), ylabel="Score")
    # D: heatmap
    M = rng.normal(0, 1, (8, 12)); M[:4, :6] += 1.5; M[4:, 6:] += 1.5
    heatmap(axd["D"], M, [f"Gene{i + 1}" for i in range(8)], [f"S{i + 1}" for i in range(12)], center=0, cbar_label="z score", italic_rows=True)
    # E: volcano
    fc = rng.normal(0, 0.9, 3000); p = 10 ** (-np.abs(fc) * rng.uniform(0.2, 2.2, 3000))
    fc[:4] = [3.4, 2.6, -3.1, -2.2]; p[:4] = [1e-9, 1e-7, 1e-8, 1e-6]
    volcano(axd["E"], fc, p, labels=[f"Gene{i + 1}" for i in range(3000)], top=4)
    # F: box
    box_points(axd["F"], {"G1": rng.normal(0, 1, 60), "G2": rng.normal(0.8, 1, 60), "G3": rng.normal(1.5, 1, 60)}, ylabel="Activity (a.u.)")
    cs.label_panels(axd)
    out = cs.save_cell(fig, Path(outdir) / "Figure 1", formats=("pdf", "tiff"), strict=strict)
    out["legend_snippet"] = leg_b
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", metavar="OUTDIR")
    ap.add_argument("--draft", action="store_true", help="export even when a gate fails")
    a = ap.parse_args()
    if a.demo:
        import json
        r = demo(a.demo, strict=not a.draft)
        print(json.dumps({k: r[k] for k in ("size_mm", "gates", "files")}, indent=1))
        for x in r.get("audit", []) if isinstance(r.get("audit"), list) else []:
            import validate_cell_figure as v
            print(v.render(x))
