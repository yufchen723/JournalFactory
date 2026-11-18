#!/usr/bin/env python3
"""cell_text_check.py - countable checks for a Cell (Cell Press) research article draft.

Standard library only; Python 3.9+.

Every limit in this file comes from cell-shared/journal-formats/cell.md (read on
cell.com 2026-11-18). The section number of that file is printed with each finding.
Heuristic checks (abbreviations, legend statistics, scale bars) are WARN only.

Usage
-----
  cell_text_check.py MANUSCRIPT.md [--stage initial|revision|final] [--type TYPE] [--json]
  cell_text_check.py --highlights HIGHLIGHTS_ETOC.md [--json]
  cell_text_check.py --self-test

Input format (manuscript mode)
------------------------------
Markdown or plain text with headings written as "# Summary", "# Introduction",
"# Results", "## A subheading", "# Discussion", "## Limitations of the study",
"# Resource availability", "# Figure titles and legends", "# STAR Methods" ...
The title is the body of a "# Title" section, or else the first level-1 heading
that is not a known section name. Legends start a line with "Figure 1." / "Figure S1.".

Counting method (Cell does not specify one; see cell.md)
--------------------------------------------------------
A word is a whitespace-separated token that contains a letter or a digit, after
Markdown markup and HTML comments are removed. Characters are counted with spaces,
after markup removal and whitespace collapsing. Word-processor counts can differ
by a few words.

Main-text count = Introduction + Results + Discussion (subheadings included)
+ main figure titles and legends. Excluded: STAR Methods, supplemental legends,
references (cell.md section 2). Summary, title and back matter are reported separately
because cell.md does not say whether they count for a research article.

Exit code: 1 if any FAIL, else 0. 2 on usage or input errors.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# Limits. Source: cell-shared/journal-formats/cell.md
# --------------------------------------------------------------------------
TITLE_MAX_CHARS = 145          # section 3
TITLE_WORDS_GUIDE = (10, 12)   # section 3, "about 10-12 words"
SUMMARY_MAX_WORDS = 150        # section 3
KEYWORDS_MAX = 10              # section 3
HIGHLIGHTS_MAX = 4             # section 6
HIGHLIGHT_MAX_CHARS = 85       # section 6
ETOC_MAX_WORDS = 50            # section 6
ETOC_MAX_SENTENCES = 2         # section 6

ARTICLE_TYPES = {
    # type: (word limit, strictly-under?, max display items)   section 2
    "research": (7000, True, 7),
    "resource": (7000, True, 7),
    "theory": (7000, True, 7),
    "matters-arising": (7000, True, 7),
    "short": (4000, False, 4),
}

STAGES = ("initial", "revision", "final")

FAIL, WARN, LATER, INFO, OK = "FAIL", "WARN", "LATER", "INFO", "OK"

# --------------------------------------------------------------------------
# Section names
# --------------------------------------------------------------------------
SECTION_ALIASES = {
    "title": ["title"],
    "summary": ["summary"],
    "abstract": ["abstract"],
    "keywords": ["keywords", "key words"],
    "introduction": ["introduction"],
    "results": ["results"],
    "discussion": ["discussion"],
    "resource availability": ["resource availability"],
    "acknowledgments": ["acknowledgments", "acknowledgements"],
    "author contributions": ["author contributions"],
    "declaration of interests": ["declaration of interests"],
    "supplemental": [
        "supplemental information titles and legends",
        "supplemental information",
        "supplemental figure titles and legends",
        "supplemental figure legends",
        "supplemental items",
    ],
    "legends": [
        "figure titles and legends",
        "main figure titles and legends",
        "figure legends",
        "main figure legends",
        "figures",
    ],
    "tables": ["tables", "main tables"],
    "star methods": ["star methods", "star★methods", "star*methods"],
    "methods": ["methods", "materials and methods", "experimental procedures"],
    "references": ["references"],
    "highlights": ["highlights"],
    "etoc": ["etoc blurb", "etoc", "in brief", "etoc blurb (in brief)", "etoc blurb in brief"],
}

RA_SUBSECTIONS = ["lead contact", "materials availability", "data and code availability"]

# STAR Methods headings: cell.md section 8 marks this list as "from the author guide,
# not re-read on 2026-11-18; confirm in the PDF". Reported as INFO only.
STAR_HEADINGS_UNVERIFIED = [
    "key resources table",
    "experimental model and study participant details",
    "method details",
    "quantification and statistical analysis",
]

HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
BOLD_LINE_RE = re.compile(r"^\s*(?:\*\*|__)(.+?)(?:\*\*|__)\s*[:.]?\s*$")
LEGEND_START_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:\*\*|__)?\s*(Figure|Table)\s+(S?)(\d+)\s*(?:\*\*|__)?\s*[.:|]", re.I
)

# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------


def strip_markup(text: str) -> str:
    """Remove Markdown/HTML markup that a word processor would not count."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]*)\)", r"\1", text)
    text = re.sub(r"</?(?:sup|sub|i|b|em|strong|u|br)\s*/?>", "", text, flags=re.I)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"\1", text)
    text = re.sub(r"(?<![\w_])_(?!\s)([^_\n]+?)(?<!\s)_(?![\w_])", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    return text


def count_words(text: str) -> int:
    return sum(1 for tok in strip_markup(text).split() if re.search(r"[A-Za-z0-9]", tok))


def clean_line(text: str) -> str:
    return re.sub(r"\s+", " ", strip_markup(text)).strip()


def norm_heading(text: str) -> str:
    t = clean_line(text).lower()
    t = re.sub(r"^\d+(\.\d+)*[.)]?\s+", "", t)
    return t.strip(" :.")


def split_sentences(text: str) -> List[str]:
    t = clean_line(text)
    protect = [
        "et al.", "e.g.", "i.e.", "vs.", "cf.", "Fig.", "Figs.", "Dr.", "ca.", "approx.", "sp.", "spp.",
    ]
    for i, p in enumerate(protect):
        t = t.replace(p, "\x00%d\x00" % i)
    t = re.sub(r"\b([A-Z])\.(?=\s+[A-Z])", "\\1\x01", t)       # initials: "J. Smith"
    t = re.sub(r"(\d)\.(\d)", "\\1\x01\\2", t)                 # decimals
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])", t)
    out = []
    for part in parts:
        for i, p in enumerate(protect):
            part = part.replace("\x00%d\x00" % i, p)
        part = part.replace("\x01", ".").strip()
        if part and re.search(r"[A-Za-z0-9]", part):
            out.append(part)
    return out


def paragraphs(text: str) -> List[str]:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return [p.strip() for p in re.split(r"\n\s*\n", text) if re.search(r"[A-Za-z0-9]", p)]


CITATION_PATTERNS = [
    (re.compile(r"\[\s*\d+(?:\s*[,\u2013\u2014-]\s*\d+)*\s*\]"), "bracketed reference number"),
    (re.compile(r"\bet al\b\.?", re.I), '"et al."'),
    (re.compile(r"\([^()]*\b(?:19|20)\d{2}[a-z]?\s*\)"), "author-year citation"),
    (re.compile(r"\[@[^\]]+\]"), "citation key"),
    (re.compile(r"<sup>\s*\d[\d,\u2013\s-]*</sup>", re.I), "superscript reference number"),
    (re.compile(r"\^\d[\d,\u2013-]*\^"), "superscript reference number"),
    (re.compile(r"(?<=[A-Za-z.,;)])[\u00b9\u00b2\u00b3\u2070\u2074-\u2079]+"), "superscript reference number"),
    (re.compile(r"\\cite\w*\{"), "LaTeX citation"),
]

NOVELTY_RE = re.compile(r"\b(novel|novelty|first|unprecedented)\b", re.I)

# Abbreviations that general life-science readers know. Cell does not publish a list of
# "standard" abbreviations (see cell.md); this allowlist only reduces noise in a WARN.
STANDARD_ABBREV = {
    "DNA", "RNA", "mRNA", "tRNA", "rRNA", "cDNA", "ATP", "ADP", "GTP", "GDP", "NAD", "NADH",
    "PCR", "CRISPR", "HIV", "UV", "pH", "US", "USA", "UK", "II", "III", "IV", "VI", "VII",
}
ABBREV_RE = re.compile(
    r"\b(?:[A-Za-z]*[A-Z][A-Za-z]*[A-Z][A-Za-z0-9]*|[A-Za-z]+\d+[A-Za-z0-9]*)(?:-[A-Za-z0-9]+)*\b"
)


def find_abbreviations(text: str) -> List[str]:
    found = []
    for m in ABBREV_RE.finditer(clean_line(text)):
        tok = m.group(0)
        head = tok.split("-")[0]
        if tok in STANDARD_ABBREV or head in STANDARD_ABBREV:
            continue
        if tok not in found:
            found.append(tok)
    return found


# --------------------------------------------------------------------------
# Document model
# --------------------------------------------------------------------------


class Heading:
    def __init__(self, level: int, text: str, line: int):
        self.level = level
        self.text = text
        self.norm = norm_heading(text)
        self.line = line
        self.end = line  # exclusive end line of the section, set later


class Doc:
    def __init__(self, text: str):
        text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
        self.lines = text.split("\n")
        self.headings: List[Heading] = []
        in_code = False
        in_comment = False
        for i, line in enumerate(self.lines):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if in_comment:
                if "-->" in line:
                    in_comment = False
                continue
            if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            m = HEADING_RE.match(line)
            if m:
                self.headings.append(Heading(len(m.group(1)), m.group(2), i))
        for idx, h in enumerate(self.headings):
            h.end = len(self.lines)
            for later in self.headings[idx + 1:]:
                if later.level <= h.level:
                    h.end = later.line
                    break

    def find(self, key: str) -> Optional[Heading]:
        aliases = SECTION_ALIASES[key]
        hits = [h for h in self.headings if h.norm in aliases]
        if not hits:
            return None
        return sorted(hits, key=lambda h: (h.level, h.line))[0]

    def body(self, h: Heading, include_subheadings: bool = True) -> str:
        lines = self.lines[h.line + 1:h.end]
        if not include_subheadings:
            lines = [ln for ln in lines if not HEADING_RE.match(ln)]
        return "\n".join(lines)

    def subheadings(self, h: Heading) -> List[Heading]:
        return [x for x in self.headings if h.line < x.line < h.end]

    def bold_lines(self, h: Heading) -> List[str]:
        out = []
        for ln in self.lines[h.line + 1:h.end]:
            m = BOLD_LINE_RE.match(ln)
            if m and len(m.group(1).split()) <= 14:
                out.append(m.group(1).strip())
        return out


class Report:
    def __init__(self, stage: str = "revision"):
        self.stage = stage
        self.items: List[Dict[str, str]] = []

    def add(self, level: str, check: str, message: str, src: str = "", min_stage: str = "initial"):
        """min_stage: earliest stage at which Cell applies the rule (cell.md section 1)."""
        if level in (FAIL, WARN) and STAGES.index(self.stage) < STAGES.index(min_stage):
            message += " [needed at %s stage]" % min_stage
            level = LATER
        self.items.append({"level": level, "check": check, "message": message, "source": src})

    def failed(self) -> bool:
        return any(i["level"] == FAIL for i in self.items)

    def count(self, level: str) -> int:
        return sum(1 for i in self.items if i["level"] == level)

    def has(self, level: str, check: str) -> bool:
        return any(i["level"] == level and i["check"] == check for i in self.items)

    def render(self, header: str) -> str:
        out = [header, "=" * len(header)]
        width = max([len(i["check"]) for i in self.items] + [5])
        for i in self.items:
            src = "  (%s)" % i["source"] if i["source"] else ""
            out.append("%-5s  %-*s  %s%s" % (i["level"], width, i["check"], i["message"], src))
        out.append("-" * len(header))
        out.append(
            "FAIL %d   WARN %d   LATER %d   -> %s"
            % (self.count(FAIL), self.count(WARN), self.count(LATER),
               "hard limit failed (exit 1)" if self.failed() else "no hard limit failed (exit 0)")
        )
        return "\n".join(out)


# --------------------------------------------------------------------------
# Legends
# --------------------------------------------------------------------------

TEST_RE = re.compile(
    r"(t[ -]test|ANOVA|Mann[- \u2013]Whitney|Wilcoxon|Kruskal|log[- ]rank|Fisher|chi[- ]squared?|"
    r"\u03c7\s?2|permutation test|Tukey|Dunnett|Bonferroni|Benjamini|Holm|Welch|Pearson|Spearman|"
    r"Kolmogorov|hypergeometric|binomial test|likelihood[- ]ratio|mixed[- ]effects|\bDESeq2?\b|"
    r"\bedgeR\b|\blimma\b|linear model|regression|bootstrap)",
    re.I,
)
PDEF_RE = re.compile(
    r"(\bp\s*(?:<|>|=|\u2264|\u2265)|\badjusted p\b|\bFDR\b|\bq\s*<|\bn\.s\.|not significant)", re.I
)
N_RE = re.compile(
    r"(\bn\s*(?:=|\u2265|>|\u2264)\s*\d|\b\d+\s+(?:biological|technical|independent)\b|"
    r"\b(?:biological|technical)\s+replicates?\b|\bindependent experiments?\b|\breplicates?\b)",
    re.I,
)
ERROR_RE = re.compile(
    r"(\u00b1|\+/-|\bSEM\b|\bS\.E\.M\.|\bSD\b|\bS\.D\.|standard deviation|standard error|"
    r"confidence intervals?|\bCI\b|error bars?|\bmedian\b|\bIQR\b|interquartile|box ?plots?|whiskers)",
    re.I,
)
SEE_ALSO_RE = re.compile(r"\bSee also\s+(?:Figures?|Tables?|Data|Videos?|Methods|Document)\s+S\d", re.I)
RELATED_RE = re.compile(r"\brelated to\s+(?:Figures?|Tables?|STAR Methods)\b", re.I)
IMAGE_RE = re.compile(
    r"(micrograph|immunofluorescence|immunohistochem|confocal|microscopy|\bH&E\b|hematoxylin|"
    r"staining|stained|representative images?|electron microscop|\bDAPI\b|live imaging|in situ hybridization)",
    re.I,
)
SCALE_RE = re.compile(r"scale bars?", re.I)
QUANT_RE = re.compile(
    r"(quantif|\bmean\b|\bmedian\b|percentage|proportion|fold change|expression level|"
    r"\u00b1|\*\s?p\b|survival|bar (?:graph|plot)|violin|box ?plot|dot plot)",
    re.I,
)


def parse_legends(text: str) -> List[Dict[str, str]]:
    """Return legends found in a block: kind (Figure/Table), supp ('S' or ''), num, text."""
    out: List[Dict[str, str]] = []
    current: Optional[Dict[str, str]] = None
    for line in text.split("\n"):
        m = LEGEND_START_RE.match(line)
        if m:
            current = {
                "kind": m.group(1).capitalize(),
                "supp": m.group(2).upper(),
                "num": m.group(3),
                "text": re.sub(r"^\s*#{1,6}\s*", "", line),
            }
            out.append(current)
        elif current is not None:
            if HEADING_RE.match(line) and not LEGEND_START_RE.match(line):
                current = None
            else:
                current["text"] += "\n" + line
    return out


def legend_label(lg: Dict[str, str]) -> str:
    return "%s %s%s" % (lg["kind"], lg["supp"], lg["num"])


def check_legend(rep: Report, lg: Dict[str, str]) -> None:
    label = legend_label(lg) + " legend"
    text = clean_line(lg["text"])
    src = "cell.md s4"
    has_test, has_p = bool(TEST_RE.search(text)), bool(PDEF_RE.search(text))
    quantitative = bool(QUANT_RE.search(text) or has_test or has_p or N_RE.search(text))
    missing = []
    if not has_test and not has_p:
        missing.append("statistical test / p value meaning")
    elif has_p and not has_test:
        missing.append("name of the statistical test")
    if not N_RE.search(text):
        missing.append("n (biological and technical replicates)")
    if not ERROR_RE.search(text):
        missing.append("definition of measure and error bars")
    if missing:
        note = "" if quantitative else " (ignore if the figure has no quantitative panel)"
        rep.add(WARN, label, "no statement found for: " + "; ".join(missing) + note, src, "revision")
    if IMAGE_RE.search(text) and not SCALE_RE.search(text):
        rep.add(WARN, label, "image panels mentioned but no scale bar defined "
                             "(fine if every bar is labeled in the image)", "cell.md s4, s5", "revision")
    if lg["supp"]:
        if not RELATED_RE.search(text):
            rep.add(WARN, label, 'title lacks "related to Figure N"', "cell.md s7", "revision")
    else:
        if not SEE_ALSO_RE.search(text):
            rep.add(WARN, label, 'no "See also Figure S…" pointer (needed if a supplemental item relates '
                                 "to this figure)", src, "revision")
        first_line = clean_line(lg["text"].strip().split("\n")[0])
        title = re.split(r"(?<=[.!?])\s", re.sub(r"^(Figure|Table)\s+\d+\s*[.:|]\s*", "", first_line), 1)[0]
        if re.search(r"\([A-Z](?:\s*(?:,|and|\u2013|-)\s*[A-Z])*\)", title):
            rep.add(WARN, label, "panel citation inside the figure title", src, "revision")


# --------------------------------------------------------------------------
# Manuscript mode
# --------------------------------------------------------------------------

TOPIC_SUBHEAD_RE = re.compile(
    r"^(analysis|analyses|characteri[sz]ation|identification|investigation|examination|evaluation|"
    r"assessment|study|studies|role|roles|effects?|overview|profiling|validation|generation|"
    r"construction|development|comparison|exploration|mapping|screening)\b\s+(of|for|in)\b",
    re.I,
)
VERB_HINT_RE = re.compile(
    r"\b(is|are|was|were|has|have|requires?|regulates?|controls?|drives?|promotes?|inhibits?|"
    r"activates?|represses?|binds?|induces?|prevents?|restores?|depletes?|defines?|marks?|"
    r"mediates?|determines?|sets?|limits?|enables?|predicts?|\w+(?:es|s))\b",
    re.I,
)
WRONG_SUPP_RE = re.compile(
    r"\b(Supplementa(?:ry|l)\s+(?:Fig(?:ure|s)?\.?|Tables?|Videos?|Movies?|Data|Notes?)\s*S?\d+|"
    r"Supplementary\s+(?:Fig(?:ure|s)?\.?|Tables?|Videos?|Movies?|Information|Materials?|Methods)|"
    r"Extended\s+Data(?:\s+(?:Fig(?:ure|s)?\.?|Tables?))?(?:\s*\d+)?)",
    re.I,
)
LOWER_PANEL_RE = re.compile(r"\bFig(?:ure|s|ures)?\.?\s+S?\d+[a-z]\b(?![a-z])")
FIG_ABBREV_RE = re.compile(r"\bFigs?\.\s*S?\d+")
_ITEM = r"S?\d+[A-Za-z]?(?:\s*[\u2013\u2014-]\s*[A-Za-z]\b)?"
_LIST = _ITEM + r"(?:\s*(?:,\s*and|,|and|to|[\u2013\u2014-])\s*" + _ITEM + r")*"
FIG_CITE_RE = re.compile(r"\bFig(?:ures?|s)?\.?\s+(" + _LIST + ")")
TABLE_CITE_RE = re.compile(r"\bTables?\s+(" + _LIST + ")")


def cited_numbers(rx: "re.Pattern", text: str) -> List[int]:
    """Main (non-S) item numbers in order of first citation; "Figures 4-8" expands to 4..8."""
    order: List[int] = []
    for m in rx.finditer(text):
        tokens = re.findall(r"S?\d+|,\s*and|,|and|to|[\u2013\u2014-]", m.group(1))
        prev: Optional[int] = None
        range_open = False
        for tok in tokens:
            if tok[0] == "S":
                prev, range_open = None, False
            elif tok.isdigit():
                k = int(tok)
                span = range(prev + 1, k + 1) if (range_open and prev is not None and prev < k <= prev + 30) else [k]
                for j in span:
                    if j not in order:
                        order.append(j)
                prev, range_open = k, False
            else:
                range_open = tok in ("to", "-", "\u2013", "\u2014")
    return order

TABLE_AB_RE = re.compile(r"\bTable\s+\d+[A-Za-z]\b")


def get_title(doc: Doc) -> Optional[str]:
    h = doc.find("title")
    if h is not None:
        for par in paragraphs(doc.body(h, include_subheadings=False)):
            return clean_line(par)
    known = set(a for v in SECTION_ALIASES.values() for a in v)
    for h in doc.headings:
        if h.level == 1 and h.norm not in known:
            return clean_line(h.text)
    return None


def check_manuscript(text: str, stage: str = "revision", article_type: str = "research") -> Report:
    rep = Report(stage)
    doc = Doc(text)
    limit, strict, max_items = ARTICLE_TYPES[article_type]

    # ---- Title -------------------------------------------------------------
    title = get_title(doc)
    if title is None:
        rep.add(WARN, "Title", 'not found (use "# Title" followed by the title, or a level-1 heading)')
    else:
        n_chars, n_words = len(title), count_words(title)
        lvl = FAIL if n_chars > TITLE_MAX_CHARS else OK
        rep.add(lvl, "Title", "%d characters with spaces (limit %d)" % (n_chars, TITLE_MAX_CHARS),
                "cell.md s3", "revision")
        lo, hi = TITLE_WORDS_GUIDE
        rep.add(WARN if n_words > hi + 3 else INFO, "Title",
                "%d words (Cell: about %d-%d words)" % (n_words, lo, hi), "cell.md s3", "revision")
        ab = find_abbreviations(title)
        if ab:
            rep.add(WARN, "Title", "possible abbreviations: %s (heuristic; gene and protein names "
                                   "may be fine)" % ", ".join(ab), "cell.md s3", "revision")
        nov = sorted(set(m.group(0).lower() for m in NOVELTY_RE.finditer(title)))
        if nov:
            rep.add(WARN, "Title", "discouraged novelty word(s): %s" % ", ".join(nov), "cell.md s3")

    # ---- Summary -----------------------------------------------------------
    summ = doc.find("summary")
    if summ is None and doc.find("abstract") is not None:
        summ = doc.find("abstract")
        rep.add(WARN, "Summary", 'section is headed "Abstract"; Cell calls it "Summary"', "cell.md s3", "revision")
    if summ is None:
        rep.add(FAIL, "Summary", 'section not found (expected "# Summary")', "cell.md s3", "revision")
    else:
        body = doc.body(summ)
        n = count_words(body)
        rep.add(FAIL if n > SUMMARY_MAX_WORDS else OK, "Summary",
                "%d words (limit %d)" % (n, SUMMARY_MAX_WORDS), "cell.md s3", "revision")
        n_par = len(paragraphs(body))
        if n_par > 1:
            rep.add(FAIL, "Summary", "%d paragraphs (must be one paragraph)" % n_par, "cell.md s3", "revision")
        cites = []
        for rx, name in CITATION_PATTERNS:
            for m in rx.finditer(body):
                cites.append("%s: %r" % (name, m.group(0).strip()[:40]))
        if cites:
            rep.add(FAIL, "Summary", "citations are not allowed; found " + "; ".join(cites[:4]),
                    "cell.md s3", "revision")
        nov = sorted(set(m.group(0).lower() for m in NOVELTY_RE.finditer(strip_markup(body))))
        if nov:
            rep.add(WARN, "Summary", 'discouraged word(s): %s (Cell: "overused ... difficult to verify"; '
                                     '"first" as an ordinal is fine)' % ", ".join(nov), "cell.md s3")
        ab = find_abbreviations(body)
        if ab:
            rep.add(WARN, "Summary", "check for non-standard abbreviations: %s (heuristic)" % ", ".join(ab[:12]),
                    "cell.md s3", "revision")

    # ---- Keywords ----------------------------------------------------------
    kw = doc.find("keywords")
    if kw is None:
        rep.add(INFO, "Keywords", "section not found (up to %d, comma separated)" % KEYWORDS_MAX, "cell.md s3")
    else:
        raw = clean_line(doc.body(kw))
        items = [k.strip() for k in re.split(r"[,;\n]", raw) if k.strip()]
        rep.add(FAIL if len(items) > KEYWORDS_MAX else OK, "Keywords",
                "%d keywords (limit %d)" % (len(items), KEYWORDS_MAX), "cell.md s3", "revision")
        if ";" in raw and "," not in raw:
            rep.add(WARN, "Keywords", "separated by semicolons; Cell asks for commas", "cell.md s3", "revision")

    # ---- Introduction ------------------------------------------------------
    intro = doc.find("introduction")
    w_intro = 0
    if intro is None:
        rep.add(WARN, "Introduction", "section not found", "cell.md s3", "revision")
    else:
        w_intro = count_words(doc.body(intro))
        subs = [h.text for h in doc.subheadings(intro)] + doc.bold_lines(intro)
        if subs:
            rep.add(FAIL, "Introduction", "%d subheading(s) found; none are allowed: %s"
                    % (len(subs), "; ".join(clean_line(s)[:50] for s in subs[:3])), "cell.md s3", "revision")
        else:
            rep.add(OK, "Introduction", "%d words, no subheadings" % w_intro, "cell.md s3")

    # ---- Results -----------------------------------------------------------
    res = doc.find("results")
    w_res = 0
    if res is None:
        rep.add(WARN, "Results", "section not found", "cell.md s3", "revision")
    else:
        w_res = count_words(doc.body(res))
        subs = [h for h in doc.subheadings(res) if h.level == min(x.level for x in doc.subheadings(res))]
        if not subs:
            rep.add(WARN, "Results", "no subheadings; Cell asks for subsections with informative subheadings",
                    "cell.md s3", "revision")
        else:
            rep.add(OK, "Results", "%d words, %d subsections" % (w_res, len(subs)), "cell.md s3")
            for h in subs:
                t = clean_line(h.text)
                if TOPIC_SUBHEAD_RE.match(t) or not VERB_HINT_RE.search(t):
                    rep.add(WARN, "Results", 'subheading may name a topic, not a finding: "%s" (heuristic)'
                            % t[:70], "cell.md s3", "revision")

    # ---- Discussion --------------------------------------------------------
    disc = doc.find("discussion")
    w_disc = 0
    lim_found = any(h.norm == "limitations of the study" for h in doc.headings)
    if disc is None:
        rep.add(WARN, "Discussion", "section not found", "cell.md s3", "revision")
    else:
        w_disc = count_words(doc.body(disc))
        inside = any(h.norm == "limitations of the study" for h in doc.subheadings(disc)) or any(
            norm_heading(b) == "limitations of the study" for b in doc.bold_lines(disc))
        if inside:
            rep.add(OK, "Discussion", '%d words, "Limitations of the study" present' % w_disc, "cell.md s3")
        elif lim_found:
            rep.add(WARN, "Discussion", '"Limitations of the study" exists but is not a subsection of the '
                                        "Discussion", "cell.md s3", "revision")
        else:
            rep.add(FAIL, "Discussion", 'missing subsection "Limitations of the study"', "cell.md s3", "revision")

    # ---- Resource availability ---------------------------------------------
    ra = doc.find("resource availability")
    if ra is None:
        rep.add(FAIL, "Resource availability", "section not found (required, with three subsections)",
                "cell.md s3", "revision")
    else:
        have = [h.norm for h in doc.subheadings(ra)] + [norm_heading(b) for b in doc.bold_lines(ra)]
        missing = [s for s in RA_SUBSECTIONS if s not in have]
        if missing:
            rep.add(FAIL, "Resource availability", "missing subsection(s): " + ", ".join(missing),
                    "cell.md s3", "revision")
        else:
            rep.add(OK, "Resource availability", "three subsections present", "cell.md s3")

    # ---- Legends and display items -----------------------------------------
    leg_sec = doc.find("legends")
    supp_sec = doc.find("supplemental")
    tab_sec = doc.find("tables")
    legends: List[Dict[str, str]] = []
    if leg_sec is not None:
        legends += parse_legends(doc.body(leg_sec))
    else:
        rep.add(WARN, "Figure legends", 'section not found (expected "# Figure titles and legends"); '
                                        "main-text count will miss the legends", "cell.md s3", "revision")
    if supp_sec is not None:
        legends += parse_legends(doc.body(supp_sec))
    table_titles = parse_legends(doc.body(tab_sec)) if tab_sec is not None else []

    main_fig = [l for l in legends if l["kind"] == "Figure" and not l["supp"]]
    supp_fig = [l for l in legends if l["kind"] == "Figure" and l["supp"]]
    main_tab = {l["num"] for l in table_titles + legends if l["kind"] == "Table" and not l["supp"]}

    # Body text used for callouts: everything except STAR Methods and references.
    excluded_spans = []
    for key in ("star methods", "methods", "references"):
        h = doc.find(key)
        if h is not None:
            excluded_spans.append((h.line, h.end))
    body_lines = [ln for i, ln in enumerate(doc.lines)
                  if not any(a <= i < b for a, b in excluded_spans)]
    body_text = strip_markup("\n".join(body_lines))

    cited_figs = sorted(cited_numbers(FIG_CITE_RE, body_text))
    cited_tabs = sorted(cited_numbers(TABLE_CITE_RE, body_text))
    n_fig = max(len({l["num"] for l in main_fig}), max(cited_figs) if cited_figs else 0)
    n_tab = max(len(main_tab), max(cited_tabs) if cited_tabs else 0)
    total_items = n_fig + n_tab
    rep.add(FAIL if total_items > max_items else OK, "Display items",
            "%d main figures + %d main tables = %d (limit %d)" % (n_fig, n_tab, total_items, max_items),
            "cell.md s2")
    if len(supp_fig) > 20:
        rep.add(WARN, "Supplemental figures", "%d (recommended no more than 20)" % len(supp_fig), "cell.md s7")

    # Callouts: every main figure cited, first citations in numerical order (main text only).
    main_text_for_order = ""
    for h in (intro, res, disc):
        if h is not None:
            main_text_for_order += strip_markup(doc.body(h)) + "\n"
    order = cited_numbers(FIG_CITE_RE, main_text_for_order)
    if order and order != sorted(order):
        rep.add(WARN, "Figure callouts", "first citations are not in numerical order: %s"
                % ", ".join(str(k) for k in order), "cell.md s4", "revision")
    legend_nums = sorted({int(l["num"]) for l in main_fig})
    uncited = [k for k in legend_nums if k not in order]
    if uncited and (intro is not None or res is not None):
        rep.add(WARN, "Figure callouts", "main figure(s) with a legend but no callout in the main text: %s"
                % ", ".join(str(k) for k in uncited), "cell.md s4", "revision")

    for lg in main_fig + supp_fig:
        check_legend(rep, lg)

    # ---- Main-text length ---------------------------------------------------
    w_leg = sum(count_words(l["text"]) for l in main_fig)
    total = w_intro + w_res + w_disc + w_leg
    over = total >= limit if strict else total > limit
    limit_txt = ("under %d" if strict else "at most %d") % limit
    rep.add(FAIL if over else OK, "Main text",
            "%d words = Introduction %d + Results %d + Discussion %d + main figure legends %d (limit: %s)"
            % (total, w_intro, w_res, w_disc, w_leg, limit_txt), "cell.md s2")
    if article_type != "short":
        rep.add(INFO, "Main text", "excluded: STAR Methods, supplemental legends, references. Not counted here and "
                                   "not specified by Cell for this article type: title, Summary, back matter",
                "cell.md s2")
    else:
        rep.add(WARN, "Main text", "short article: Cell also counts title, authors, affiliations and summary; "
                                   "add them by hand", "cell.md s2")
    if not over and total > limit - 200:
        rep.add(WARN, "Main text", "within 200 words of the limit; counting methods differ", "cell.md s2")

    # ---- STAR Methods -------------------------------------------------------
    star = doc.find("star methods")
    if star is None:
        if doc.find("methods") is not None:
            rep.add(FAIL, "STAR Methods", 'methods section is not headed "STAR Methods" '
                                          "(STAR Methods format is required at revision)", "cell.md s8", "revision")
        else:
            rep.add(FAIL, "STAR Methods", "section not found (required at revision)", "cell.md s8", "revision")
    else:
        have = [h.norm for h in doc.subheadings(star)]
        missing = [s for s in STAR_HEADINGS_UNVERIFIED if s not in have]
        if missing:
            rep.add(INFO, "STAR Methods", "headings not found: %s. This heading list is from the author guide "
                                          "and was not re-read on 2026-11-18; confirm in the PDF"
                    % ", ".join(missing), "cell.md s8")
        else:
            rep.add(OK, "STAR Methods", "present with the expected headings (list unverified; confirm in the "
                                        "author guide PDF)", "cell.md s8")
        if not re.search(r"RRID\s*:", doc.body(star)):
            rep.add(WARN, "STAR Methods", "no RRID found (required for antibodies and genetically modified "
                                          "organisms, if any are used)", "cell.md s8", "revision")

    # ---- Wording ------------------------------------------------------------
    whole = strip_markup("\n".join(doc.lines))
    wrong = [m.group(0) for m in WRONG_SUPP_RE.finditer(whole)]
    if wrong:
        uniq = sorted(set(re.sub(r"\s+", " ", w) for w in wrong))
        rep.add(FAIL, "Supplemental naming", '%d instance(s) of non-Cell naming: %s -> use "Figure S1", '
                                             '"Table S1", "Video S1", "Data S1", "Methods S1"'
                % (len(wrong), "; ".join(uniq[:5])), "cell.md s7", "revision")
    else:
        rep.add(OK, "Supplemental naming", 'no "Supplementary Figure" / "Extended Data" wording', "cell.md s7")
    lower = sorted(set(m.group(0) for m in LOWER_PANEL_RE.finditer(whole)))
    if lower:
        rep.add(WARN, "Panel letters", "lowercase panel letters in callouts: %s (Cell panels are capital letters)"
                % ", ".join(lower[:6]), "cell.md s5", "revision")
    figabbr = FIG_ABBREV_RE.findall(whole)
    if figabbr:
        rep.add(INFO, "Figure callouts", '%d callout(s) use "Fig."; cell.md writes "Figure 1" / "Figure S1" '
                                         "throughout (abbreviation not specified by Cell)" % len(figabbr), "cell.md s4")
    tab_ab = sorted(set(TABLE_AB_RE.findall(whole)))
    if tab_ab:
        rep.add(WARN, "Tables", 'split table labels are not allowed: %s' % ", ".join(tab_ab[:5]),
                "cell.md s4", "revision")
    return rep


# --------------------------------------------------------------------------
# Highlights / eTOC mode
# --------------------------------------------------------------------------

BULLET_RE = re.compile(r"^\s*(?:[-*+\u2022\u00b7]|\d+[.)])\s+(.*\S)\s*$")
FIRST_PERSON_RE = re.compile(r"\b(we|our|ours|us|i|my)\b", re.I)


def split_highlights_file(text: str) -> Tuple[List[str], str]:
    doc = Doc(text)
    hl, et = doc.find("highlights"), doc.find("etoc")
    if hl is not None or et is not None:
        hl_body = doc.body(hl) if hl is not None else ""
        et_body = doc.body(et, include_subheadings=False) if et is not None else ""
        if hl is None:
            pre = "\n".join(doc.lines[:et.line]) if et is not None else ""
            hl_body = pre
        bullets = []
        for ln in re.sub(r"<!--.*?-->", " ", hl_body, flags=re.S).split("\n"):
            m = BULLET_RE.match(ln)
            if m:
                bullets.append(m.group(1))
            elif hl is not None and ln.strip() and not HEADING_RE.match(ln):
                bullets.append(ln.strip())
        et_lines = [ln for ln in re.sub(r"<!--.*?-->", " ", et_body, flags=re.S).split("\n")]
        return bullets, " ".join(l.strip() for l in et_lines if l.strip())
    bullets, rest = [], []
    for ln in re.sub(r"<!--.*?-->", " ", text, flags=re.S).split("\n"):
        m = BULLET_RE.match(ln)
        if m:
            bullets.append(m.group(1))
        elif ln.strip() and not HEADING_RE.match(ln):
            rest.append(ln.strip())
    return bullets, " ".join(rest)


def check_highlights(text: str) -> Report:
    rep = Report("final")
    bullets, etoc = split_highlights_file(text)
    src = "cell.md s6"
    if not bullets:
        rep.add(FAIL, "Highlights", 'no bullets found (use "- " lines under "# Highlights")', src)
    else:
        rep.add(FAIL if len(bullets) > HIGHLIGHTS_MAX else OK, "Highlights",
                "%d bullets (limit %d)" % (len(bullets), HIGHLIGHTS_MAX), src)
        for i, b in enumerate(bullets, 1):
            c = clean_line(b)
            n = len(c)
            rep.add(FAIL if n > HIGHLIGHT_MAX_CHARS else OK, "Highlight %d" % i,
                    "%d characters with spaces (limit %d)%s"
                    % (n, HIGHLIGHT_MAX_CHARS, "; %d over" % (n - HIGHLIGHT_MAX_CHARS) if n > HIGHLIGHT_MAX_CHARS else ""),
                    src)
            ab = find_abbreviations(c)
            if re.search(r"\b(e\.g\.|i\.e\.|vs\.?|etc\.)", c):
                ab.append("e.g./i.e./vs./etc.")
            if ab:
                rep.add(WARN, "Highlight %d" % i, "possible abbreviation(s): %s (none allowed; heuristic, "
                                                  "gene symbols also match)" % ", ".join(ab), src)
            if any(rx.search(b) for rx, _ in CITATION_PATTERNS[:1] + CITATION_PATTERNS[3:6]):
                rep.add(WARN, "Highlight %d" % i, "looks like a citation", "craft")
            nov = sorted(set(m.group(0).lower() for m in NOVELTY_RE.finditer(c)))
            if nov:
                rep.add(WARN, "Highlight %d" % i, "discouraged word(s): %s" % ", ".join(nov), "cell.md s3")
    if not etoc.strip():
        rep.add(FAIL, "eTOC blurb", 'not found (put it under "# In brief" or "# eTOC blurb")', src)
    else:
        n = count_words(etoc)
        rep.add(FAIL if n > ETOC_MAX_WORDS else OK, "eTOC blurb", "%d words (limit %d)" % (n, ETOC_MAX_WORDS), src)
        sents = split_sentences(etoc)
        rep.add(FAIL if len(sents) > ETOC_MAX_SENTENCES else OK, "eTOC blurb",
                "%d sentence(s) (limit %d)" % (len(sents), ETOC_MAX_SENTENCES), src)
        fp = sorted(set(m.group(0).lower() for m in FIRST_PERSON_RE.finditer(clean_line(etoc))))
        if fp:
            rep.add(FAIL, "eTOC blurb", "first person found (%s); must be third person" % ", ".join(fp), src)
        else:
            rep.add(OK, "eTOC blurb", "third person", src)
        ab = find_abbreviations(etoc)
        if ab:
            rep.add(WARN, "eTOC blurb", "check abbreviations for a general audience: %s (heuristic)"
                    % ", ".join(ab[:8]), src)
        nov = sorted(set(m.group(0).lower() for m in NOVELTY_RE.finditer(clean_line(etoc))))
        if nov:
            rep.add(WARN, "eTOC blurb", "discouraged word(s): %s" % ", ".join(nov), "cell.md s3")
    return rep


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

_GOOD = """# Title
A dose-dependent damage signal matches stem cell output to tissue need

# Summary
Tissues must replace damaged cells, but how stem cells sense damage is unclear. Here, we show that
factor X sets the number of stem cells that divide after injury in the mouse intestine.

# Keywords
stem cells, tissue repair, damage sensing

# Introduction
Tissues lose cells every day.^1^ How repair scales with damage is unknown. Here, we show that factor X
scales repair (Figure 1A).

# Results
## Dying cells release factor X in proportion to damage
Factor X rose with dose (Figure 1A; Figure S1A).

## Factor X is required for stem cell activation
Deletion blocked activation (Figure 2B; Table 1).

# Discussion
The signal is dose dependent.

## Limitations of the study
We deleted factor X in all epithelial cells; the relevant source cell type is not resolved.

# Resource availability
## Lead contact
Requests go to the lead contact.
## Materials availability
Lines are available on request.
## Data and code availability
Data are deposited.

# Supplemental information titles and legends
Figure S1. Factor X dose response in a second strain, related to Figure 1
(A) Factor X level. n = 4 mice per group; mean ± SEM; *p < 0.05 by Student's t test.

# Figure titles and legends
Figure 1. Dying cells release factor X in proportion to damage
(A) Factor X level after irradiation. n = 5 mice per group, one experiment of three shown.
Data are represented as mean ± SEM. *p < 0.05 by Student's t test. See also Figure S1.

Figure 2. Factor X is required for stem cell activation
(A) Immunofluorescence of intestinal crypts. Scale bars, 50 µm.
(B) Quantification of dividing stem cells. n = 6 mice per group. Data are represented as
mean ± SD. **p < 0.01 by two-way ANOVA. See also Figure S1.

# STAR Methods
## Key resources table
Anti-factor X antibody, RRID: AB_0000000.
## Experimental model and study participant details
Mice.
## Method details
Irradiation. This sentence is in STAR Methods and must not be counted in the main text at all.
## Quantification and statistical analysis
Tests are listed in the legends.

# References
1. Author, A., and Author, B. (2020). A title. Journal 1, 1–2.
"""

_BAD = """# A novel analysis reveals for the first time how the factor X and receptor Y signaling axis controls every aspect of ISC activation and tissue repair in vivo

# Abstract
First paragraph cites prior work [1,2] and (Smith et al., 2020).

Second paragraph is novel.

# Keywords
a; b; c; d; e; f; g; h; i; j; k

# Introduction
## Background
Text (Supplementary Figure 1a). See Extended Data Fig. 2 and Fig. 3b.

# Results
## Analysis of factor X
Text (Figure 8A; Table 2).

# Discussion
No limitations here.

# Methods
Text.

# Figure legends
**Figure 1. Characterization of factor X (A and B)**
(A) Confocal images of crypts.
"""

_HL_GOOD = """# Highlights
- Dying epithelial cells release factor X in proportion to tissue damage
- Factor X binds receptor Y on quiescent stem cells to trigger division

# In brief
How stem cells measure tissue damage has been unclear. Lee et al. show that factor X, released by
dying epithelial cells, activates intestinal stem cells in proportion to injury.
"""

_HL_BAD = """- We show that FX-RY signaling in ISCs is the first dose-dependent sensor of tissue damage in the gut epithelium
- two
- three
- four
- five

We found a signal. It scales repair. It protects our stem cells.
"""


def self_test() -> int:
    results: List[Tuple[str, bool]] = []

    def t(name: str, cond: bool) -> None:
        results.append((name, bool(cond)))

    t("count_words plain", count_words("Factor X binds receptor Y.") == 5)
    t("count_words markup", count_words("**Factor** *X* binds [receptor Y](http://x) <!-- hidden words -->") == 5)
    t("count_words symbols not counted", count_words("mean ± SEM, n = 5") == 4)
    t("clean_line strips emphasis", clean_line("*Fx* is  required") == "Fx is required")
    t("sentences: et al.", len(split_sentences("Lee et al. show that X acts. It scales repair.")) == 2)
    t("sentences: decimals", len(split_sentences("The value was 2.5 fold. Done.")) == 2)
    t("callouts: ranges and lists",
      cited_numbers(FIG_CITE_RE, "Figures 1A and 1B; Figure S9; Figures 4\u20136; Figure 2A-C; Figs. 7 and 8")
      == [1, 4, 5, 6, 2, 7, 8])
    t("abbreviation heuristic", find_abbreviations("ISC and scRNA-seq with DNA") == ["ISC", "scRNA-seq"])

    good = check_manuscript(_GOOD)
    t("good: no FAIL", not good.failed())
    t("good: title 70 chars", any(i["check"] == "Title" and i["message"].startswith("70 characters") for i in good.items))
    t("good: summary counted", any(i["check"] == "Summary" and i["message"].startswith("33 words") for i in good.items))
    t("good: 2 figures + 1 table", any("2 main figures + 1 main tables = 3" in i["message"] for i in good.items))
    t("good: STAR Methods excluded from main text",
      any(i["check"] == "Main text" and "Introduction 22 + Results 33 + Discussion 25 + main figure legends 88" in i["message"]
          for i in good.items))
    t("good: no legend warnings", not any(i["check"].endswith("legend") for i in good.items))

    bad = check_manuscript(_BAD)
    msgs = {(i["level"], i["check"]) for i in bad.items}
    t("bad: title too long", (FAIL, "Title") in msgs)
    t("bad: novelty in title", any(i["check"] == "Title" and "novelty" in i["message"] for i in bad.items))
    t("bad: summary citations", any(i["level"] == FAIL and "citations" in i["message"] for i in bad.items))
    t("bad: summary two paragraphs", any(i["level"] == FAIL and "paragraphs" in i["message"] for i in bad.items))
    t("bad: 11 keywords", (FAIL, "Keywords") in msgs)
    t("bad: intro subheading", (FAIL, "Introduction") in msgs)
    t("bad: limitations missing", (FAIL, "Discussion") in msgs)
    t("bad: resource availability missing", (FAIL, "Resource availability") in msgs)
    t("bad: display items 8 + 2", any(i["level"] == FAIL and "8 main figures + 2 main tables" in i["message"]
                                      for i in bad.items))
    t("bad: supplementary wording", (FAIL, "Supplemental naming") in msgs)
    t("bad: lowercase panels", (WARN, "Panel letters") in msgs)
    t("bad: topic subheading", any(i["check"] == "Results" and "topic" in i["message"] for i in bad.items))
    t("bad: legend warnings", sum(1 for i in bad.items if i["check"] == "Figure 1 legend") >= 3)
    t("bad: STAR Methods heading", (FAIL, "STAR Methods") in msgs)
    t("legend: p value without a test name",
      any("name of the statistical test" in i["message"] for i in check_manuscript(
          "# Figure legends\nFigure 1. X requires Y\n(A) Counts. n = 3 mice. Mean \u00b1 SD. *p < 0.05. See also Figure S1.\n"
      ).items))

    initial = check_manuscript(_BAD, stage="initial")
    t("initial stage: structure rules become LATER",
      initial.has(LATER, "Introduction") and initial.has(LATER, "STAR Methods"))
    t("initial stage: length/display limits still FAIL", initial.has(FAIL, "Display items"))

    long_text = _GOOD.replace("The signal is dose dependent.", "word " * 7000)
    t("7,000-word limit", check_manuscript(long_text).has(FAIL, "Main text"))
    t("short article limit 4 items", ARTICLE_TYPES["short"][2] == 4)

    hg = check_highlights(_HL_GOOD)
    t("highlights good: no FAIL", not hg.failed())
    hb = check_highlights(_HL_BAD)
    t("highlights bad: 5 bullets", hb.has(FAIL, "Highlights"))
    t("highlights bad: >85 chars", hb.has(FAIL, "Highlight 1"))
    t("highlights bad: abbreviations", hb.has(WARN, "Highlight 1"))
    t("etoc bad: 3 sentences + first person",
      sum(1 for i in hb.items if i["check"] == "eTOC blurb" and i["level"] == FAIL) == 2)
    exact = "- " + "x" * 85 + "\n\nOne sentence here.\n"
    t("85 characters passes", not check_highlights(exact).has(FAIL, "Highlight 1"))
    t("86 characters fails", check_highlights(exact.replace("x" * 85, "x" * 86)).has(FAIL, "Highlight 1"))
    t("50-word eTOC passes", not check_highlights("- a b\n\n" + "word " * 49 + "end.").failed())
    t("51-word eTOC fails", check_highlights("- a b\n\n" + "word " * 50 + "end.").failed())

    width = max(len(n) for n, _ in results)
    for name, ok in results:
        print("%-*s  %s" % (width, name, "ok" if ok else "FAILED"))
    n_bad = sum(1 for _, ok in results if not ok)
    print("-" * (width + 8))
    print("self-test: %d/%d passed" % (len(results) - n_bad, len(results)))
    return 1 if n_bad else 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Check a Cell research-article draft against the countable rules in "
                    "cell-shared/journal-formats/cell.md.")
    ap.add_argument("manuscript", nargs="?", help="Markdown or plain-text manuscript")
    ap.add_argument("--highlights", metavar="FILE", help="check a highlights + eTOC blurb file instead")
    ap.add_argument("--stage", choices=STAGES, default="revision",
                    help="initial: format rules are reported as LATER (cell.md s1). Default: revision")
    ap.add_argument("--type", dest="article_type", choices=sorted(ARTICLE_TYPES), default="research",
                    help="article type for the length and display-item limits (cell.md s2)")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    ap.add_argument("--self-test", action="store_true", help="run the built-in tests and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.manuscript and not args.highlights:
        ap.print_usage(sys.stderr)
        return 2

    reports = []
    try:
        if args.manuscript:
            reports.append(("Cell manuscript check: %s (stage: %s, type: %s)"
                            % (args.manuscript, args.stage, args.article_type),
                            check_manuscript(read_text(args.manuscript), args.stage, args.article_type)))
        if args.highlights:
            reports.append(("Cell highlights / eTOC check: %s" % args.highlights,
                            check_highlights(read_text(args.highlights))))
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([{"title": t, "failed": r.failed(), "findings": r.items} for t, r in reports], indent=2,
                         ensure_ascii=False))
    else:
        print("\n\n".join(r.render(t) for t, r in reports))
    return 1 if any(r.failed() for _, r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
