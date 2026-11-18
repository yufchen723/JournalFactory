#!/usr/bin/env python3
"""Mechanical checks on a Cell point-by-point response written in Markdown.

Checks
  1. Every reviewer comment block has a response and a manuscript location
     (or an explicit "No change to the manuscript" with a reason).
  2. With --manuscript: every figure, panel and table named in the authors'
     text exists in the manuscript's legends (reviewer quotes are skipped,
     because they refer to the old numbering).
  3. Lists promises ("we will", "future work", ...) so each one is either
     done or removed before submission.

Expected response layout (templates/point_by_point.md):

    ## Reviewer 1
    ### Comment R1.1
    > reviewer text, verbatim
    **Response:** ...
    **Changes in the manuscript:** Results, "subheading", paragraph 2; Figure 3C.

A comment block starts at a heading or bold line carrying an ID (R1.2, E.1), or
at "### Comment 2" under a "## Reviewer 1" heading.

Usage:
    check_response_package.py response.md [--manuscript manuscript.md] [--json]
    check_response_package.py --self-test

Standard library only. Python 3.9+. No network access. Exit 1 on any ERROR.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REVIEWER_HEAD = re.compile(r"^\s*#{1,6}\s*(?:\*\*)?\s*(Reviewer|Referee)\s*#?\s*(\d+)\b", re.IGNORECASE)
EDITOR_HEAD = re.compile(r"^\s*#{1,6}\s*(?:\*\*)?\s*Editor\b", re.IGNORECASE)
COMMENT_ID = re.compile(r"^\s*(?:#{1,6}\s*|\*\*\s*)(?:Comment\s+)?((?:R\d+|E)[.\-]\d+[a-z]?)\b", re.IGNORECASE)
COMMENT_NUM = re.compile(r"^\s*(?:#{1,6}\s*|\*\*\s*)(?:Comment|Point)\s+(\d+)\b", re.IGNORECASE)
RESPONSE_LABEL = re.compile(r"^\s*(?:[-*]\s*)?\**\s*(?:Author(?:s'|s|')?\s+)?(?:Response|Reply)\s*\**\s*:\s*\**\s*(.*)$", re.IGNORECASE)
LOCATION_LABEL = re.compile(
    r"^\s*(?:[-*]\s*)?\**\s*(?:Changes?(?: in the (?:revised )?manuscript)?|Location|Where in (?:the )?manuscript|Manuscript location)\s*\**\s*:\s*\**\s*(.*)$",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(
    r"AUTHOR_INPUT_NEEDED|\bTBD\b|\bTODO\b|\bXX+\b|^\s*\.{3}\s*$|"
    r"\[[^\]]*(?:location|page|line|figure|text|answer|reason|comment|xx)[^\]]*\](?!\()|"
    r"\[[^\]]*[a-z]{3,}[^\]]*[\s.][^\]]*\](?!\()",
    re.IGNORECASE,
)
NO_CHANGE = re.compile(r"no changes? (?:to|in|was made to|were made to) the manuscript|manuscript (?:is )?unchanged", re.IGNORECASE)
PROMISE = re.compile(
    r"\bwe will\b|\bwe plan to\b|\bwe intend to\b|\bwill be (?:added|performed|included|provided|deposited|addressed|uploaded|made available)\b|"
    r"\bfuture (?:work|stud(?:y|ies)|experiments?|investigations?)\b|\bfollow[- ]up (?:work|stud(?:y|ies)|paper|manuscript)\b|"
    r"\bin progress\b|\bongoing\b|\bunderway\b|\bis planned\b|\bare planned\b",
    re.IGNORECASE,
)
FIG_PREFIX = re.compile(r"\b(Figures?|Figs?\.?|Tables?)\s+(?=S?\d)")
TOKEN = re.compile(r"(S?\d+)([A-Z](?![A-Za-z]))?(?:\s*[–-]\s*([A-Z])(?![A-Za-z]))?")
SEP = re.compile(r"\s*(?:,\s*and\s+|,\s*|\s+and\s+|\s+or\s+)")
BARE_PANEL = re.compile(r"([A-Z])(?![A-Za-z\d])(?:\s*[–-]\s*([A-Z])(?![A-Za-z]))?")
LEGEND_START = re.compile(r"^\s*(?:#{1,6}\s*)?(?:\*\*|__)?\s*(Figure|Table)\s+(S?\d+)\s*(?:\*\*|__)?\s*[.:|]", re.IGNORECASE)
PANEL_IN_LEGEND = re.compile(r"\(([A-Z](?:(?:\s*,\s*(?:and\s+)?|\s+and\s+|\s*[–-]\s*)[A-Z])*)\)")


def _span(a: str, b: Optional[str]) -> List[str]:
    if not b or ord(b) < ord(a):
        return [a]
    return [chr(c) for c in range(ord(a), ord(b) + 1)]


def find_refs(text: str) -> List[Tuple[str, str, Optional[str]]]:
    """Return (kind, number, panel-or-None) for each figure/table reference in text."""
    refs: List[Tuple[str, str, Optional[str]]] = []
    for m in FIG_PREFIX.finditer(text):
        kind = "Table" if m.group(1).lower().startswith("tab") else "Figure"
        pos = m.end()
        current: Optional[str] = None
        while True:
            t = TOKEN.match(text, pos)
            if t:
                current = t.group(1).upper()
                if t.group(2) and kind == "Figure":
                    for p in _span(t.group(2), t.group(3)):
                        refs.append((kind, current, p))
                else:
                    refs.append((kind, current, None))
                pos = t.end()
            elif current is not None and kind == "Figure":
                b = BARE_PANEL.match(text, pos)
                if not b:
                    break
                for p in _span(b.group(1), b.group(2)):
                    refs.append((kind, current, p))
                pos = b.end()
            else:
                break
            s = SEP.match(text, pos)
            if not s:
                break
            nxt = s.end()
            if not (TOKEN.match(text, nxt) or (kind == "Figure" and BARE_PANEL.match(text, nxt))):
                break
            pos = nxt
    return refs


def parse_manuscript(text: str) -> Dict[str, Dict[str, Set[str]]]:
    """Map 'Figure'/'Table' -> number -> set of panel letters found in the legend."""
    items: Dict[str, Dict[str, Set[str]]] = {"Figure": {}, "Table": {}}
    current: Optional[Set[str]] = None
    for line in text.splitlines():
        m = LEGEND_START.match(line)
        if m:
            kind = m.group(1).capitalize()
            current = items[kind].setdefault(m.group(2).upper(), set())
            if kind == "Table":
                current = None
                continue
        elif re.match(r"^\s*#{1,6}\s", line):
            current = None
        if current is not None:
            for pm in PANEL_IN_LEGEND.finditer(line):
                letters = re.findall(r"[A-Z]", re.sub(r"\band\b", " ", pm.group(1)))
                if re.search(r"[–-]", pm.group(1)) and len(letters) == 2:
                    current.update(_span(letters[0], letters[1]))
                else:
                    current.update(letters)
    return items


def parse_response(text: str) -> List[Dict[str, object]]:
    blocks: List[Dict[str, object]] = []
    reviewer: Optional[str] = None
    block: Optional[Dict[str, object]] = None
    field: Optional[str] = None
    for lineno, line in enumerate(text.splitlines(), 1):
        rh = REVIEWER_HEAD.match(line)
        if rh or EDITOR_HEAD.match(line):
            reviewer = f"R{rh.group(2)}" if rh else "E"
            block, field = None, None
            continue
        cid = COMMENT_ID.match(line)
        cnum = None if cid else COMMENT_NUM.match(line)
        if cid or (cnum and reviewer):
            ident = cid.group(1).upper().replace("-", ".") if cid else f"{reviewer}.{cnum.group(1)}"
            block = {"id": ident, "line": lineno, "comment": [], "response": [], "location": [], "author_lines": []}
            blocks.append(block)
            field = None
            continue
        if block is None:
            continue
        if re.match(r"^\s*#{1,6}\s", line):
            block, field = None, None
            continue
        if line.lstrip().startswith(">"):
            block["comment"].append(line.lstrip()[1:].strip())
            continue
        rl = RESPONSE_LABEL.match(line)
        ll = None if rl else LOCATION_LABEL.match(line)
        if rl:
            field = "response"
            rest = rl.group(1)
        elif ll:
            field = "location"
            rest = ll.group(1)
        else:
            rest = line
        if field and rest.strip():
            block[field].append(rest.strip())
            block["author_lines"].append((lineno, rest))
    return blocks


def check(response_text: str, manuscript_text: Optional[str] = None) -> Dict[str, object]:
    findings: List[Dict[str, object]] = []
    promises: List[Dict[str, object]] = []
    blocks = parse_response(response_text)

    def add(level: str, code: str, where: str, message: str) -> None:
        findings.append({"level": level, "code": code, "where": where, "message": message})

    if not blocks:
        add("ERROR", "NO_COMMENT_BLOCKS", "response",
            "no comment blocks found; use headings such as '### Comment R1.1' (see templates/point_by_point.md)")
    seen: Set[str] = set()
    for b in blocks:
        ident = str(b["id"])
        where = f"{ident} (line {b['line']})"
        if ident in seen:
            add("ERROR", "DUPLICATE_ID", where, "comment ID is used twice")
        seen.add(ident)
        if not " ".join(b["comment"]).strip():
            add("WARN", "NO_QUOTED_COMMENT", where, "no quoted reviewer text ('> ...') under this comment")
        response = " ".join(b["response"]).strip()
        location = " ".join(b["location"]).strip()
        if not response:
            add("ERROR", "NO_RESPONSE", where, "no 'Response:' text")
        elif PLACEHOLDER.search(response):
            add("ERROR", "PLACEHOLDER_IN_RESPONSE", where, "response still contains a placeholder")
        if not location:
            add("ERROR", "NO_LOCATION", where,
                "no 'Changes in the manuscript:' line; give the location or write 'No change to the manuscript' with the reason")
        elif PLACEHOLDER.search(location):
            add("ERROR", "PLACEHOLDER_IN_LOCATION", where, "manuscript location is still a placeholder")
        elif NO_CHANGE.search(location) and len(location.split()) < 8:
            add("WARN", "NO_CHANGE_WITHOUT_REASON", where, "'No change to the manuscript' needs a one-line reason")
        for lineno, text in b["author_lines"]:
            for pm in PROMISE.finditer(text):
                promises.append({"id": ident, "line": lineno, "phrase": pm.group(0), "text": text.strip()[:140]})

    # sequence gaps per reviewer
    by_rev: Dict[str, List[int]] = {}
    for ident in seen:
        rev, _, num = ident.partition(".")
        digits = re.match(r"\d+", num)
        if digits:
            by_rev.setdefault(rev, []).append(int(digits.group(0)))
    for rev, nums in sorted(by_rev.items()):
        gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
        if gaps:
            add("WARN", "ID_GAP", rev, "comment numbers missing: " + ", ".join(f"{rev}.{g}" for g in gaps))

    if manuscript_text is not None:
        items = parse_manuscript(manuscript_text)
        if not items["Figure"]:
            add("WARN", "NO_LEGENDS_FOUND", "manuscript", "no 'Figure N.' legend lines found; figure references were not checked")
        else:
            reported: Set[Tuple[str, str, Optional[str]]] = set()
            for b in blocks:
                for lineno, text in b["author_lines"]:
                    for kind, number, panel in find_refs(text):
                        key = (kind, number, panel)
                        if key in reported:
                            continue
                        where = f"{b['id']} (line {lineno})"
                        if kind == "Table":
                            if items["Table"] and number not in items["Table"]:
                                reported.add(key)
                                add("ERROR", "TABLE_NOT_IN_MANUSCRIPT", where, f"Table {number} has no title line in the manuscript")
                            continue
                        if number not in items["Figure"]:
                            if (kind, number, None) not in reported:
                                reported.add((kind, number, None))
                                add("ERROR", "FIGURE_NOT_IN_MANUSCRIPT", where, f"Figure {number} has no legend in the manuscript")
                        elif panel and items["Figure"][number] and panel not in items["Figure"][number]:
                            reported.add(key)
                            add("ERROR", "PANEL_NOT_IN_LEGEND", where,
                                f"Figure {number}{panel}: the legend of Figure {number} has panels "
                                f"{''.join(sorted(items['Figure'][number]))} only")
    # de-duplicate identical findings
    unique, keys = [], set()
    for f in findings:
        k = (f["code"], f["where"], f["message"])
        if k not in keys:
            keys.add(k)
            unique.append(f)
    return {"comments": len(blocks), "findings": unique, "promises": promises}


def print_report(result: Dict[str, object]) -> int:
    findings = result["findings"]
    errors = [f for f in findings if f["level"] == "ERROR"]
    print(f"Comment blocks: {result['comments']}")
    print(f"Findings: {len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
    for f in findings:
        print(f"  [{f['level']}] {f['code']} at {f['where']}: {f['message']}")
    promises = result["promises"]
    print(f"Promises to resolve before submission: {len(promises)}")
    for p in promises:
        print(f"  {p['id']} line {p['line']}: \"{p['phrase']}\" in: {p['text']}")
    print("Mechanical check only: it does not judge whether a response answers the comment.")
    return 1 if errors else 0


RESPONSE_OK = """\
# Response to reviewers

## Reviewer 1

### Comment R1.1
> The claim that factor X acts upstream of factor Y rests on one knockdown.

**Response:** We agree. We repeated the experiment with a second, independent guide and a rescue construct (Figures 2C and 2D, and Figure S2A–C).

**Changes in the manuscript:** Results, "Factor X acts upstream of factor Y", paragraph 2; Figure 2C, D; Figure S2; Table S1.

### Comment R1.2
> Figure 5F lacks a scale bar.

**Response:** Corrected.

**Changes in the manuscript:** Figure 3B.

## Reviewer 2

### Comment 1
> Please discuss the limits of the model system.

**Response:** We added this to "Limitations of the study".

**Changes in the manuscript:** Discussion, Limitations of the study, sentences 2-3.
"""

RESPONSE_BAD = """\
## Reviewer 1

### Comment R1.1
> Please quantify panel B.

**Response:** We will add the quantification in Figure 4E and Figure 9A. A cohort analysis is left for future work.

### Comment R1.3
> Define the error bars.

**Response:**

**Changes in the manuscript:** [location]
"""

MANUSCRIPT = """\
## Figure titles and legends

Figure 1. Factor X marks cell type A
(A and B) Design. (C) Counts.

Figure 2. Factor X acts upstream of factor Y
(A) Scheme. (B) Blot. (C and D) Rescue.

Figure 3. Localization
(A) Overview. (B) Zoom.

Figure 4. Dose response
(A–D) Curves.

Figure S2. Guides, related to Figure 2
(A–C) Validation.

Table S1. Guide sequences, related to Figure 2
"""


def self_test() -> int:
    failures: List[str] = []
    refs = find_refs("see Figures 2C and 2D, Figure S2A–C, Figure 2C, D and Table S1. Figure 3 And then Figure 5.")
    expect_refs = [("Figure", "2", "C"), ("Figure", "2", "D"), ("Figure", "S2", "A"), ("Figure", "S2", "B"),
                   ("Figure", "S2", "C"), ("Figure", "2", "C"), ("Figure", "2", "D"), ("Table", "S1", None),
                   ("Figure", "3", None), ("Figure", "5", None)]
    if refs != expect_refs:
        failures.append(f"find_refs: got {refs}")
    items = parse_manuscript(MANUSCRIPT)
    if items["Figure"].get("4") != set("ABCD") or items["Figure"].get("1") != set("ABC") or "S1" not in items["Table"]:
        failures.append(f"parse_manuscript: got {items}")
    ok = check(RESPONSE_OK, MANUSCRIPT)
    if ok["comments"] != 3:
        failures.append(f"OK case: expected 3 comment blocks, got {ok['comments']}")
    if [f for f in ok["findings"] if f["level"] == "ERROR"]:
        failures.append(f"OK case should have no errors: {ok['findings']}")
    if ok["promises"]:
        failures.append(f"OK case should have no promises: {ok['promises']}")
    bad = check(RESPONSE_BAD, MANUSCRIPT)
    codes = {f["code"] for f in bad["findings"]}
    for code in ("NO_LOCATION", "NO_RESPONSE", "PLACEHOLDER_IN_LOCATION", "PANEL_NOT_IN_LEGEND", "FIGURE_NOT_IN_MANUSCRIPT", "ID_GAP"):
        if code not in codes:
            failures.append(f"BAD case: expected {code}, got {sorted(codes)}")
    phrases = {p["phrase"].lower() for p in bad["promises"]}
    if not {"we will", "future work"} <= phrases:
        failures.append(f"BAD case: promises not listed: {phrases}")
    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("self-test passed: reference parser, legend parser, complete response, deficient response")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Mechanical checks on a Cell point-by-point response (Markdown).")
    parser.add_argument("response", nargs="?", help="response to reviewers, Markdown")
    parser.add_argument("--manuscript", help="revised manuscript, Markdown or plain text, containing the figure legends")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.response:
        parser.error("give a response file or --self-test")
    response_text = Path(args.response).read_text(encoding="utf-8", errors="replace")
    manuscript_text = Path(args.manuscript).read_text(encoding="utf-8", errors="replace") if args.manuscript else None
    result = check(response_text, manuscript_text)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if any(f["level"] == "ERROR" for f in result["findings"]) else 0
    return print_report(result)


if __name__ == "__main__":
    sys.exit(main())
