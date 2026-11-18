#!/usr/bin/env python3
"""Format and lint references in Cell style.

Cell rule (cell-shared/journal-formats/cell.md, section 9):
  - numbered in order of first citation;
  - "et al." only after 10 author names;
  - Sondheimer, N., and Lindquist, S. (2000). Rnq1: an epigenetic modifier of
    protein function in yeast. Mol. Cell 5, 163–172. 10.1016/S1097-2765(00)80412-8.
  - preprints allowed with a DOI ("Preprint at bioRxiv, ...").

Commands
  format  refs.json [--number]   JSON or CSL-JSON list -> Cell-style lines
  check   refs.txt  [--json]     lint a plain-text list, one reference per line
  --self-test

The script never looks anything up. It formats what it is given; it does not
verify that a reference exists (see references/verification.md) and it does not
abbreviate journal names (supply "container-title-short" or "journal_abbrev").

Standard library only. Python 3.9+. No network access.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAX_AUTHORS = 10  # cell.md section 9: "et al." only after 10 author names
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+")
PREPRINT_SERVERS = ("biorxiv", "medrxiv", "arxiv", "research square", "ssrn", "chemrxiv", "preprints.org")


# ----------------------------------------------------------------- format

def initials(given: str) -> str:
    """'Susan L.' -> 'S.L.'; 'Jean-Pierre' -> 'J.-P.'; 'S L' -> 'S.L.'."""
    given = given.strip()
    if not given:
        return ""
    out = []
    for part in re.split(r"[\s.]+", given.replace("-", " -")):
        if not part:
            continue
        if part.startswith("-"):
            if len(part) > 1:
                out.append("-" + part[1].upper() + ".")
        elif part.isupper() and len(part) <= 3 and "." not in given and " " not in given:
            out.extend(ch + "." for ch in part)  # 'SL' -> 'S.L.'
        else:
            out.append(part[0].upper() + ".")
    return "".join(out)


def author_name(author) -> str:
    if isinstance(author, str):
        text = author.strip()
        if "," in text:
            family, given = text.split(",", 1)
            return f"{family.strip()}, {initials(given)}" if given.strip() else family.strip()
        parts = text.split()
        if len(parts) == 1:
            return text
        return f"{parts[-1]}, {initials(' '.join(parts[:-1]))}"
    if "literal" in author:
        return str(author["literal"]).strip()
    family = " ".join(x for x in (author.get("non-dropping-particle", ""), author.get("family", "")) if x).strip()
    given = initials(str(author.get("given", "")))
    suffix = author.get("suffix", "")
    name = f"{family}, {given}" if given else family
    return f"{name}, {suffix}" if suffix else name


def author_list(authors: List) -> str:
    names = [author_name(a) for a in authors if a]
    names = [n for n in names if n]
    if not names:
        return ""
    if len(names) > MAX_AUTHORS:
        return ", ".join(names[:MAX_AUTHORS]) + ", et al."
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", and " + names[-1]


def _first(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def _year(entry: Dict) -> str:
    if entry.get("year"):
        return str(entry["year"])
    for key in ("issued", "published", "published-print", "published-online"):
        parts = (entry.get(key) or {}).get("date-parts")
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def _doi(entry: Dict) -> str:
    raw = str(entry.get("DOI") or entry.get("doi") or "").strip()
    raw = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", raw, flags=re.IGNORECASE)
    return raw.rstrip(".")


def format_entry(entry: Dict) -> Tuple[str, List[str]]:
    """Return (reference line, problems)."""
    problems: List[str] = []
    authors = author_list(entry.get("author") or entry.get("authors") or [])
    year = _year(entry)
    title = str(_first(entry.get("title"))).strip().rstrip(".")
    journal = str(
        _first(entry.get("journal_abbrev")) or _first(entry.get("container-title-short"))
        or _first(entry.get("journalAbbreviation")) or _first(entry.get("journal")) or _first(entry.get("container-title"))
    ).strip()
    volume = str(entry.get("volume") or "").strip()
    pages = str(entry.get("pages") or entry.get("page") or entry.get("article-number") or "").strip()
    pages = re.sub(r"\s*-+\s*", "–", pages)
    doi = _doi(entry)
    kind = str(entry.get("type") or "").lower()
    is_preprint = "preprint" in kind or any(s in journal.lower() for s in PREPRINT_SERVERS) or kind == "posted-content"

    if journal and not is_preprint and not (
            entry.get("journal_abbrev") or entry.get("container-title-short") or entry.get("journalAbbreviation")):
        problems.append(f"journal name not abbreviated by this script: '{journal}'")
    for label, value in (("authors", authors), ("year", year), ("title", title)):
        if not value:
            problems.append(f"missing {label}")
    if not doi:
        problems.append("missing DOI" + (" (a preprint needs one)" if is_preprint else ""))

    line = f"{authors} ({year})." if authors else f"({year})."
    line += f" {title}." if title and title[-1] not in "?!" else f" {title}"
    if is_preprint:
        server = journal or str(entry.get("publisher") or "").strip()
        if not server:
            problems.append("missing preprint server")
        line += f" Preprint at {server}," if server else " Preprint,"
        line += f" {doi}." if doi else ""
    else:
        if not journal:
            problems.append("missing journal")
        tail = journal
        if volume:
            tail += f" {volume}"
        elif journal:
            problems.append("missing volume")
        if pages:
            tail += f", {pages}"
        elif journal:
            problems.append("missing pages or article number")
        if tail:
            line += f" {tail}."
        if doi:
            line += f" {doi}."
    return line.rstrip(","), problems


def cmd_format(path: str, number: bool) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("items") or data.get("references") or [data]
    status = 0
    for i, entry in enumerate(data, 1):
        line, problems = format_entry(entry)
        print(f"{i}. {line}" if number else line)
        for p in problems:
            status = 1 if p.startswith("missing") else status
            print(f"  ! entry {i}: {p}", file=sys.stderr)
    return status


# ------------------------------------------------------------------ check

LEAD_NUM = re.compile(r"^\s*(?:\[(\d+)([a-z])?\]|\((\d+)([a-z])?\)|(\d+)([a-z])?[.)])\s+")
YEAR_PAREN = re.compile(r"\((\d{4})([a-z])?\)")
INITIALS_TOKEN = re.compile(r"^(?:[A-Z]\.-?\s?)+$")
ET_AL = re.compile(r"\bet al\b\.?", re.IGNORECASE)


def split_number(line: str) -> Tuple[Optional[int], Optional[str], str]:
    m = LEAD_NUM.match(line)
    if not m:
        return None, None, line.strip()
    num = m.group(1) or m.group(3) or m.group(5)
    letter = m.group(2) or m.group(4) or m.group(6)
    return int(num), letter, line[m.end():].strip()


def count_authors(author_part: str) -> int:
    """Count 'Surname, A.B.' units: an initials token preceded by a surname token."""
    text = ET_AL.sub("", author_part)
    text = re.sub(r",?\s+and\s+", ", ", text)
    tokens = [t.strip() for t in text.split(",") if t.strip()]
    count = 0
    for prev, tok in zip(tokens, tokens[1:]):
        if INITIALS_TOKEN.match(tok) and not INITIALS_TOKEN.match(prev) and not re.search(r"\b[A-Z]\.", prev):
            count += 1
    return count


def check_line(text: str) -> List[Tuple[str, str, str]]:
    """Findings for one reference without its leading number: (level, code, message)."""
    out: List[Tuple[str, str, str]] = []
    ym = YEAR_PAREN.search(text)
    author_part = ""
    if not ym:
        out.append(("ERROR", "YEAR_NOT_IN_PARENTHESES", "no '(year)'; Cell puts the year in parentheses after the authors"))
    else:
        rest = text[ym.end():].strip(" .")
        if len(rest) < 15 or not re.match(r"\.", text[ym.end():]):
            out.append(("ERROR", "YEAR_POSITION", "'(year).' must follow the author list, before the title"))
        else:
            author_part = text[:ym.start()].strip()
        if ym.group(2):
            out.append(("WARN", "YEAR_LETTER", f"year with a letter '({ym.group(1)}{ym.group(2)})' belongs to author-date styles; Cell references are numbered"))
    if author_part:
        n = count_authors(author_part)
        has_etal = bool(ET_AL.search(author_part))
        if "&" in author_part:
            out.append(("ERROR", "AMPERSAND", "use 'and', not '&', before the last author"))
        if n == 0 and not has_etal:
            out.append(("ERROR", "AUTHOR_FORMAT", "authors are not 'Surname, A.B.' (surname first, initials with periods, no spaces)"))
        if re.search(r"\b[A-Z]\.\s[A-Z]\.", author_part):
            out.append(("WARN", "INITIALS_SPACED", "initials are written without spaces: 'A.B.', not 'A. B.'"))
        if has_etal:
            if n < MAX_AUTHORS:
                out.append(("ERROR", "ET_AL_TOO_EARLY", f"'et al.' after {n} name(s); Cell allows it only after {MAX_AUTHORS} author names"))
            elif n > MAX_AUTHORS:
                out.append(("WARN", "ET_AL_LATE", f"{n} names before 'et al.'; cell.md says after {MAX_AUTHORS}"))
        else:
            if n >= 2 and not re.search(r",\s+and\s+[^,]+,\s*(?:[A-Z]\.-?)+\s*$", author_part):
                out.append(("ERROR", "NO_AND_BEFORE_LAST", "no ', and ' before the last author"))
            if n > MAX_AUTHORS:
                out.append(("WARN", "MORE_THAN_10_AUTHORS", f"{n} authors listed in full; Cell uses 'et al.' after {MAX_AUTHORS} names"))
    doi = DOI_RE.search(text)
    if not doi:
        out.append(("WARN", "NO_DOI", "no DOI; the Cell example ends with the DOI (required for preprints, datasets and code where one exists)"))
    elif re.search(r"doi\.org/|doi:\s*10\.", text, re.IGNORECASE):
        out.append(("WARN", "DOI_FORM", "the Cell example gives the bare DOI (10.xxxx/...), without 'https://doi.org/' or 'doi:'"))
    if re.search(r"preprint|biorxiv|medrxiv|arxiv", text, re.IGNORECASE):
        if not re.search(r"Preprint at ", text):
            out.append(("WARN", "PREPRINT_FORM", "preprint entries read 'Preprint at <server>, <DOI>'"))
        out.append(("INFO", "PREPRINT", "preprint: check whether a published version exists and replace it"))
    if re.search(r"unpublished|personal communication|in preparation|manuscript submitted", text, re.IGNORECASE):
        out.append(("ERROR", "NOT_LISTABLE", "unpublished data and personal communications are cited in the text only, not in the list"))
    if not text.rstrip().endswith("."):
        out.append(("INFO", "NO_FINAL_PERIOD", "entry does not end with a period"))
    return out


def _dup_key(text: str) -> Tuple[str, str]:
    doi = DOI_RE.search(text)
    doi_key = doi.group(0).rstrip(".").lower() if doi else ""
    ym = YEAR_PAREN.search(text)
    first = re.split(r",", text, 1)[0].strip().lower()
    title = re.sub(r"[^a-z0-9]+", "", text[ym.end():].lower())[:40] if ym else ""
    text_key = f"{first}|{ym.group(1) if ym else ''}|{title}" if title else ""
    return doi_key, text_key


def check_text(text: str) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    seen_doi: Dict[str, int] = {}
    seen_text: Dict[str, int] = {}
    numbers: List[int] = []
    unnumbered = 0
    index = 0
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        index += 1
        num, letter, body = split_number(raw)
        label = f"ref {num}{letter or ''}" if num is not None else f"entry {index}"

        def add(level: str, code: str, message: str) -> None:
            findings.append({"line": lineno, "ref": label, "level": level, "code": code, "message": message})

        if num is None:
            unnumbered += 1
        else:
            if letter:
                add("ERROR", "LETTERED_PART", f"'{num}{letter}': give each reference its own number (lettered parts are not in the Cell style)")
            elif numbers and num != numbers[-1] + 1:
                add("WARN", "NUMBER_SEQUENCE", f"number {num} follows {numbers[-1]}; references are numbered in order of first citation")
            if not letter:
                numbers.append(num)
        for level, code, message in check_line(body):
            add(level, code, message)
        doi_key, text_key = _dup_key(body)
        if doi_key and doi_key in seen_doi:
            add("ERROR", "DUPLICATE", f"same DOI as the entry on line {seen_doi[doi_key]}")
        elif text_key and text_key in seen_text:
            add("ERROR", "DUPLICATE", f"same first author, year and title as the entry on line {seen_text[text_key]}")
        if doi_key:
            seen_doi.setdefault(doi_key, lineno)
        if text_key:
            seen_text.setdefault(text_key, lineno)
    if numbers and unnumbered:
        findings.append({"line": 0, "ref": "list", "level": "WARN", "code": "MIXED_NUMBERING",
                         "message": f"{unnumbered} entr(y/ies) without a number in a numbered list"})
    if numbers and numbers[0] != 1:
        findings.append({"line": 0, "ref": "list", "level": "WARN", "code": "NUMBER_START", "message": f"list starts at {numbers[0]}, not 1"})
    return findings


def cmd_check(path: str, as_json: bool) -> int:
    findings = check_text(Path(path).read_text(encoding="utf-8", errors="replace"))
    errors = sum(1 for f in findings if f["level"] == "ERROR")
    if as_json:
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            where = f"line {f['line']}, {f['ref']}" if f["line"] else f["ref"]
            print(f"[{f['level']}] {f['code']} ({where}): {f['message']}")
        print(f"{errors} error(s), {sum(1 for f in findings if f['level'] == 'WARN')} warning(s), "
              f"{sum(1 for f in findings if f['level'] == 'INFO')} note(s).")
        print("Style lint only: it does not verify that any reference exists or is correct.")
    return 1 if errors else 0


# -------------------------------------------------------------- self-test

OFFICIAL = ("Sondheimer, N., and Lindquist, S. (2000). Rnq1: an epigenetic modifier of protein function in yeast. "
            "Mol. Cell 5, 163–172. 10.1016/S1097-2765(00)80412-8.")


def self_test() -> int:
    failures: List[str] = []

    def expect(name: str, got, want) -> None:
        if got != want:
            failures.append(f"{name}:\n      got  {got!r}\n      want {want!r}")

    # format: the official example, from CSL-JSON and from the simple form
    csl = {"type": "article-journal",
           "author": [{"family": "Sondheimer", "given": "Neal"}, {"family": "Lindquist", "given": "Susan"}],
           "issued": {"date-parts": [[2000, 1]]},
           "title": "Rnq1: an epigenetic modifier of protein function in yeast.",
           "container-title": "Molecular Cell", "container-title-short": "Mol. Cell",
           "volume": "5", "page": "163-172", "DOI": "https://doi.org/10.1016/S1097-2765(00)80412-8"}
    expect("format CSL", format_entry(csl), (OFFICIAL, []))
    simple = {"authors": ["Sondheimer, N.", "Susan Lindquist"], "year": 2000,
              "title": "Rnq1: an epigenetic modifier of protein function in yeast",
              "journal_abbrev": "Mol. Cell", "volume": 5, "pages": "163–172", "doi": "10.1016/S1097-2765(00)80412-8"}
    expect("format simple", format_entry(simple)[0], OFFICIAL)
    expect("initials", [initials(x) for x in ("Susan L.", "Jean-Pierre", "A B", "SL", "Mary")],
           ["S.L.", "J.-P.", "A.B.", "S.L.", "M."])
    many = [{"family": f"Author{i}", "given": "A B"} for i in range(1, 13)]
    al = author_list(many)
    expect("et al. after 10", (al.count("Author"), al.endswith("Author10, A.B., et al.")), (10, True))
    ten = author_list(many[:10])
    expect("10 authors in full", ("et al." in ten, ten.endswith(", and Author10, A.B.")), (False, True))
    expect("three authors", author_list(many[:3]), "Author1, A.B., Author2, A.B., and Author3, A.B.")
    pre = {"type": "preprint", "authors": ["Author, A."], "year": 2024, "title": "Factor X in cell type A",
           "journal": "bioRxiv", "doi": "10.1101/2024.01.01.000000"}
    expect("preprint", format_entry(pre), ("Author, A. (2024). Factor X in cell type A. Preprint at bioRxiv, 10.1101/2024.01.01.000000.", []))
    line, problems = format_entry({"authors": ["Author, A."], "year": 2020, "title": "T", "journal": "Journal Name"})
    expect("missing fields", sorted(p.split(":")[0] for p in problems),
           ["journal name not abbreviated by this script", "missing DOI", "missing pages or article number", "missing volume"])

    # check
    expect("check official", check_text("1. " + OFFICIAL), [])

    def codes(text: str) -> set:
        return {f["code"] for f in check_text(text)}

    nature_style = "1. Sondheimer, N. & Lindquist, S. Rnq1: an epigenetic modifier of protein function in yeast. Mol. Cell 5, 163–172 (2000)."
    expect("year at end", {"YEAR_POSITION", "NO_DOI"} <= codes(nature_style), True)
    expect("no and", "NO_AND_BEFORE_LAST" in codes("Sondheimer, N., Lindquist, S. (2000). Rnq1: an epigenetic modifier. Mol. Cell 5, 163–172. 10.1016/x."), True)
    expect("ampersand", "AMPERSAND" in codes("Sondheimer, N., & Lindquist, S. (2000). Rnq1: an epigenetic modifier. Mol. Cell 5, 163–172. 10.1016/x."), True)
    expect("et al. early", "ET_AL_TOO_EARLY" in codes("Author, A.B., Author, C., et al. (2021). A title of a paper here. J. Name 1, 1–2. 10.1000/abc."), True)
    full12 = ", ".join(f"Name{chr(65 + i)}, A.B." for i in range(11)) + ", and NameL, A.B."
    expect("more than 10", "MORE_THAN_10_AUTHORS" in codes(full12 + " (2021). A title of a paper here. J. Name 1, 1–2. 10.1000/abc."), True)
    etal10 = ", ".join(f"Name{chr(65 + i)}, A.B." for i in range(10)) + ", et al."
    expect("et al. ok", codes(etal10 + " (2021). A title of a paper here. J. Name 1, 1–2. 10.1000/abc."), set())
    expect("initials first", "AUTHOR_FORMAT" in codes("N. Sondheimer and S. Lindquist (2000). Rnq1: an epigenetic modifier. Mol. Cell 5, 163–172. 10.1016/x."), True)
    dup = "1. " + OFFICIAL + "\n2. " + OFFICIAL.replace("10.1016/S1097-2765(00)80412-8", "10.1016/s1097-2765(00)80412-8")
    expect("duplicate", "DUPLICATE" in codes(dup), True)
    expect("lettered", "LETTERED_PART" in codes("12a. " + OFFICIAL), True)
    expect("sequence", "NUMBER_SEQUENCE" in codes("1. " + OFFICIAL + "\n3. Author, A. (2020). Another title of a paper. J. Name 2, 3–4. 10.1000/zzz."), True)
    expect("doi form", "DOI_FORM" in codes(OFFICIAL.replace("10.1016", "https://doi.org/10.1016")), True)
    expect("preprint note", {"PREPRINT"} <= codes("Author, A. (2024). Factor X in cell type A. Preprint at bioRxiv, 10.1101/2024.01.01.000000."), True)
    expect("personal communication", "NOT_LISTABLE" in codes("Author, A. (2024). Personal communication."), True)

    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("self-test passed: format (official example, CSL-JSON, simple JSON, initials, 10-author rule, preprint, "
          "missing fields) and check (14 lint cases)")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Format and lint references in Cell style (no network access).")
    parser.add_argument("--self-test", action="store_true")
    sub = parser.add_subparsers(dest="command")
    p_format = sub.add_parser("format", help="JSON / CSL-JSON list -> Cell-style reference lines")
    p_format.add_argument("json_file")
    p_format.add_argument("--number", action="store_true", help="prefix '1. ', '2. ' in input order")
    p_check = sub.add_parser("check", help="lint a plain-text reference list (one reference per line)")
    p_check.add_argument("text_file")
    p_check.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.command == "format":
        return cmd_format(args.json_file, args.number)
    if args.command == "check":
        return cmd_check(args.text_file, args.json)
    parser.error("give a command (format, check) or --self-test")
    return 2


if __name__ == "__main__":
    sys.exit(main())
