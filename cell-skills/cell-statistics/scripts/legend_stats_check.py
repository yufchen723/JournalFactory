#!/usr/bin/env python3
"""Check Cell figure legends for the statistics a legend must state.

Cell rule (cell-shared/journal-formats/cell.md, section 4): legends, main and
supplemental, state the statistical test(s), the p value each asterisk stands
for, the number of biological and technical replicates, what every measure and
error bar is, and related supplemental items ("See also Figure S1").
Section 7: supplemental figure titles end "related to Figure N".

This is a text lint. It cannot see the image. A clean result means the wording
is present, not that the statistics are right.

Usage:
    legend_stats_check.py legends.md            # text report, exit 1 if any WARN
    legend_stats_check.py legends.md --json
    legend_stats_check.py --self-test

Standard library only. Python 3.9+. No network access.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

LEGEND_START = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:\*\*|__)?\s*(Figure|Table)\s+(S?\d+)\s*(?:\*\*|__)?\s*[.:|]",
    re.IGNORECASE,
)

TEST = re.compile(
    r"t[- ]tests?|anova|mann[- ]whitney|wilcoxon|kruskal|friedman test|log[- ]rank|"
    r"fisher'?s? exact|chi[- ]squared?|χ2|permutation test|likelihood[- ]ratio|wald test|"
    r"mixed[- ](?:effects?)? ?model|linear model|logistic regression|cox (?:model|regression|proportional)|"
    r"pearson|spearman|kendall|hypergeometric|binomial test|kolmogorov|"
    r"dunnett|tukey|bonferroni|holm|[šs]id[aá]k|benjamini|false discovery rate|\bfdr\b|"
    r"deseq2|edger|limma|bootstrap|z[- ]test|f[- ]test|gsea|moran",
    re.IGNORECASE,
)
STAR_DEF = re.compile(r"\*{1,4}\s*(?:adjusted\s+|adj\.\s*)?[pPqQ]\s*(?:adj\.?\s*)?(?:<|≤|=|&lt;)\s*0?\.\d+")
NS_USED = re.compile(r"\bn\.?s\.?\b(?!\w)")
NS_DEF = re.compile(r"\bn\.?s\.?,?\s*(?:=|:|,|\(|indicates|denotes|means)?\s*not significant|not significant\s*\(n\.?s\.?\)", re.IGNORECASE)
EXACT_P = re.compile(r"\b[pPqQ]\s*=\s*(?:0?\.\d+|\d(?:\.\d+)?\s*[×x]\s*10)")
STAT_SIGNAL = re.compile(
    r"\*\s*[pP]\b|\b[pPqQ]\s*(?:<|≤|=)|significan|error bars?|±|\bSEM\b|s\.e\.m\.|\bSD\b|s\.d\.|compared (?:with|to)|\bversus\b|\bvs\.?\b",
    re.IGNORECASE,
)
N_STMT = re.compile(r"(?<![A-Za-z])[nN]\s*(?:=|≥|>=|>)\s*\d[\d,]*(?:\s*(?:–|-|to)\s*\d[\d,]*)?")
BIO_UNIT = re.compile(
    r"\b(?:mice|mouse|animals?|rats?|patients?|donors?|individuals?|participants?|subjects?|"
    r"samples?|specimens?|tumou?rs?|biopsies|embryos?|litters?|cohorts?|sections?|slides?|"
    r"biological(?:ly independent)? (?:replicates?|samples?|repeats?)|"
    r"independent (?:experiments?|cultures?|replicates?|differentiations?|preparations?|repeats?|transfections?)|"
    r"organoid lines?|cell lines?|clones?|flies|worms|zebrafish|fish|larvae|plants?|replicates?|experiments?)\b",
    re.IGNORECASE,
)
SUB_UNIT = re.compile(
    r"\b(?:cells|nuclei|spots?|pixels?|beads?|bins?|voxels?|fields(?: of view)?|images?|ROIs?|"
    r"regions of interest|metacells?|neurons|synapses|spines|puncta|mitochondria|droplets|barcodes|tiles?|"
    r"neighbou?rhoods?)\b"
)
REPL_KIND = re.compile(r"biological|technical|independent(?:ly)?\b", re.IGNORECASE)
ERR_BAR_WORD = re.compile(r"error bars?", re.IGNORECASE)
MEASURE_DEF = re.compile(
    r"mean\s*(?:±|\+/-|\+-|and)\s*(?:SEM|SD|s\.e\.m\.|s\.d\.|standard|95\s*%|CI)|"
    r"median\s*(?:±|\+/-|and|with)\s*(?:IQR|interquartile|range|95\s*%|MAD)|"
    r"(?:error bars?|whiskers?|boxe?s?|box ?plots?|shaded (?:areas?|regions?|bands?)|bands?|centre lines?|center lines?|bars?)\s*"
    r"(?:show|indicate|represent|denote|are|is|extend|span|,)[^.;]{0,80}"
    r"(?:SEM|SD|s\.e\.m\.|s\.d\.|standard (?:error|deviation)|confidence interval|\bCI\b|IQR|interquartile|quartile|median|mean|range|percentile)|"
    r"(?:SEM|SD|s\.e\.m\.|s\.d\.|standard (?:error|deviation)|95\s*% (?:CI|confidence interval)|IQR|interquartile range)",
    re.IGNORECASE,
)
SEE_ALSO = re.compile(r"See also\s+(?:Figures?|Tables?|Data|Videos?|Methods|Document)\s+S\d", re.IGNORECASE)
RELATED_TO = re.compile(r"related to (?:Figures?|Tables?|STAR Methods)\s*\d*", re.IGNORECASE)
IMAGE_WORD = re.compile(
    r"micrograph|microscop|immunofluorescence|immunohistochem|\bIHC\b|\bIF\b|H&E|hematoxylin|confocal|staining|stained|representative images?",
    re.IGNORECASE,
)
SCALE_BAR = re.compile(r"scale bars?", re.IGNORECASE)


def split_legends(text: str) -> List[Dict[str, str]]:
    """Split a file into legends. A legend starts at a line 'Figure 1.' / 'Figure S2.' / 'Table 1.'."""
    legends: List[Dict[str, str]] = []
    current = None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = LEGEND_START.match(line)
        if m:
            current = {
                "kind": m.group(1).capitalize(),
                "number": m.group(2).upper(),
                "line": str(lineno),
                "title_line": line.strip(),
                "body": line.strip(),
            }
            legends.append(current)
        elif current is not None:
            if re.match(r"^\s*#{1,6}\s", line):  # another heading ends the legend
                current = None
            else:
                current["body"] += "\n" + line
    return legends


def _clean(body: str) -> str:
    text = body.replace("\\*", "*").replace("&lt;", "<")
    text = re.sub(r"(?<![\w*])[*_]([nNpP])[*_](?![\w*])", r"\1", text)  # *n* -> n, *p* -> p
    return text


def _sentences(text: str) -> List[str]:
    flat = re.sub(r"\s+", " ", text)
    return [s for s in re.split(r"(?<=[.;])\s+(?=[A-Z(*])", flat) if s.strip()]


def check_legend(legend: Dict[str, str]) -> List[Tuple[str, str, str]]:
    """Return findings as (level, code, message). Levels: WARN, INFO."""
    out: List[Tuple[str, str, str]] = []
    if legend["kind"] != "Figure":
        return out
    body = _clean(legend["body"])
    supplemental = legend["number"].startswith("S")
    signals = bool(STAT_SIGNAL.search(body))

    # 1. test name
    if not TEST.search(body):
        if signals:
            out.append(("WARN", "NO_TEST", "comparisons or p values are mentioned but no statistical test is named"))
        else:
            out.append(("INFO", "NO_TEST", "no statistical test named; fine only if every panel is descriptive"))

    # 2. asterisks
    star_def = bool(STAR_DEF.search(body))
    if not star_def:
        if EXACT_P.search(body):
            out.append(("INFO", "NO_ASTERISK_KEY", "exact p values given, no asterisk key; add one if the image shows asterisks"))
        elif signals:
            out.append(("WARN", "NO_ASTERISK_KEY", "no p value given for each asterisk (e.g. '*p < 0.05, **p < 0.01')"))
        else:
            out.append(("INFO", "NO_ASTERISK_KEY", "no asterisk key; needed if the image shows asterisks"))
    if NS_USED.search(body) and not NS_DEF.search(body):
        out.append(("WARN", "NS_UNDEFINED", "'ns' is used but not defined as 'not significant'"))

    # 3. n
    n_matches = list(N_STMT.finditer(body))
    if not n_matches:
        out.append(("WARN", "NO_N", "no 'n = ...' statement; give the number of biological and technical replicates"))
    else:
        sub_only: List[str] = []
        no_unit: List[str] = []
        for sentence in _sentences(body):
            if not N_STMT.search(sentence):
                continue
            probe = re.sub(r"technical (?:replicates?|repeats?)", " ", sentence, flags=re.IGNORECASE)
            has_bio = bool(BIO_UNIT.search(probe))
            has_sub = bool(SUB_UNIT.search(re.sub(r"cell (?:lines?|types?)", " ", sentence)))
            if has_sub and not has_bio:
                sub_only.append(sentence.strip()[:110])
            elif not has_sub and not has_bio:
                no_unit.append(sentence.strip()[:110])
        for s in sub_only:
            out.append(("WARN", "N_SUBUNIT_ONLY",
                        "n is given in cells/spots/fields only; add the biological unit (animals, patients, "
                        f"independent experiments): \"{s}\""))
        for s in no_unit:
            out.append(("INFO", "N_NO_UNIT", f"n has no unit that this script recognises: \"{s}\""))
        if not REPL_KIND.search(body):
            out.append(("INFO", "REPLICATE_KIND",
                        "n is given but the legend never says biological, technical or independent"))

    # 4. measures and error bars
    if not MEASURE_DEF.search(body):
        if ERR_BAR_WORD.search(body) or signals:
            out.append(("WARN", "NO_ERROR_BAR_DEF", "no definition of the measure and error bars (e.g. 'Data are represented as mean ± SEM')"))
        else:
            out.append(("INFO", "NO_ERROR_BAR_DEF", "no measure/error-bar definition; needed if any panel shows a summary or spread"))

    # 5. links between main and supplemental items
    if supplemental:
        if not RELATED_TO.search(legend["title_line"]) and not RELATED_TO.search(body[:400]):
            out.append(("WARN", "NO_RELATED_TO", "supplemental figure title does not say 'related to Figure N'"))
    elif not SEE_ALSO.search(body):
        out.append(("WARN", "NO_SEE_ALSO", "no 'See also Figure S…'; add it if a supplemental item relates to this figure"))

    # 6. scale bars
    if IMAGE_WORD.search(body) and not SCALE_BAR.search(body):
        out.append(("INFO", "SCALE_BAR", "images are described but no scale bar is given in the legend; it must then be labelled in the image"))
    return out


def run(text: str) -> List[Dict[str, object]]:
    report = []
    for legend in split_legends(text):
        findings = check_legend(legend)
        report.append({
            "legend": f"{legend['kind']} {legend['number']}",
            "line": int(legend["line"]),
            "findings": [{"level": lv, "code": code, "message": msg} for lv, code, msg in findings],
        })
    return report


def print_report(report: List[Dict[str, object]]) -> int:
    warns = 0
    if not report:
        print("No legends found. A legend must start on its own line with 'Figure 1.' or 'Figure S1.'.")
        return 2
    for item in report:
        findings = item["findings"]
        if item["legend"].startswith("Table"):
            continue
        n_warn = sum(1 for f in findings if f["level"] == "WARN")
        warns += n_warn
        status = "OK" if not findings else f"{n_warn} warning(s), {len(findings) - n_warn} note(s)"
        print(f"{item['legend']} (line {item['line']}): {status}")
        for f in findings:
            print(f"  [{f['level']}] {f['code']}: {f['message']}")
    print(f"\n{sum(1 for i in report if i['legend'].startswith('Figure'))} figure legend(s) checked, {warns} warning(s).")
    print("Text lint only: it does not see the image and does not judge whether a test is appropriate.")
    return 1 if warns else 0


GOOD = """\
Figure 1. Factor X is required for expansion of cell type A
(A) Scheme of the experiment.
(B) Fraction of cell type A in control and factor X knockout mice (n = 6 mice per group; each dot is one mouse, mean of 2 technical replicates).
(C) Representative immunofluorescence images. Scale bars, 50 um.
(D) Signal intensity per cell (n = 1,240 cells from 5 mice per group; the test used per-mouse means).
Data are represented as mean ± SEM. *p < 0.05, **p < 0.01 by two-tailed Welch's t test (B) or linear mixed model with mouse as random effect (D). ns, not significant.
See also Figure S1 and Table S1.

Figure S1. Validation of the factor X knockout, related to Figure 1
(A) Western blot from n = 3 independent experiments (biological replicates).
Data are represented as mean ± SD. *p < 0.05 by paired t test.
"""

BAD = """\
Figure 2. Analysis of factor X
(A) Intensity in control and treated groups (n = 350 cells). Error bars are shown.
(B) Representative images of stained tissue. ***, ns.

Figure S2. More data
(A) Counts per group.
"""


def self_test() -> int:
    failures: List[str] = []
    good = run(GOOD)
    if len(good) != 2:
        failures.append(f"expected 2 legends in GOOD, got {len(good)}")
    for item in good:
        warns = [f for f in item["findings"] if f["level"] == "WARN"]
        if warns:
            failures.append(f"GOOD {item['legend']} should have no warnings: {warns}")
    bad = {item["legend"]: {f["code"] for f in item["findings"] if f["level"] == "WARN"} for item in run(BAD)}
    expect = {
        "Figure 2": {"NO_TEST", "NO_ASTERISK_KEY", "NS_UNDEFINED", "N_SUBUNIT_ONLY", "NO_ERROR_BAR_DEF", "NO_SEE_ALSO"},
        "Figure S2": {"NO_N", "NO_RELATED_TO"},
    }
    for name, codes in expect.items():
        missing = codes - bad.get(name, set())
        if missing:
            failures.append(f"BAD {name}: expected warnings not raised: {sorted(missing)} (got {sorted(bad.get(name, set()))})")
    if "NO_SEE_ALSO" in bad.get("Figure S2", set()):
        failures.append("supplemental legend must not be asked for 'See also'")
    md = run("**Figure 3.** Title\n(A) *n* = 4 patients. \\*p < 0.05 by Mann-Whitney test. Boxes show median and IQR.\nSee also Figure S3.\n")
    md_warns = [f for f in md[0]["findings"] if f["level"] == "WARN"] if md else ["not parsed"]
    if md_warns:
        failures.append(f"Markdown legend should pass: {md_warns}")
    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("self-test passed: 3 cases (complete legends, deficient legends, Markdown markup)")
    return 0


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("legends", nargs="?", help="text or Markdown file with the figure legends")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--self-test", action="store_true", help="run built-in checks and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.legends:
        parser.error("give a legends file or --self-test")
    text = Path(args.legends).read_text(encoding="utf-8", errors="replace")
    report = run(text)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if any(f["level"] == "WARN" for item in report for f in item["findings"]) else 0
    return print_report(report)


if __name__ == "__main__":
    sys.exit(main())
