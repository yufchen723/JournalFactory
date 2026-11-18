# Stage 1 · Learning a field from its papers

Purpose: before any Introduction, Discussion or journal choice, know what the field has shown, what it argues about, what the closest papers did, and what a "first" claim would have to survive. Output is a **field map** that later stages cite, not a reading diary.

Design borrowed from: PaperLens (the lab's own; paper types, story by figure, cited-by tracking, reading log, legal full text only), luwill/research-skills `lit-search` (frozen protocol, gold set, saturation), nature-paper-card (evidence and provenance labels), K-Dense `paper-lookup` and `literature-review` (endpoints, "group by themes"). Sources and licences in `10_skills_catalogue.md`.

## 1. Protocol first (write `fields/<slug>/field.json` before searching)

- **Question** the scan must answer for this paper, in one or two lines.
- **Scope**: years, organisms, tumour type, modalities in and out.
- **3–6 concept blocks** → `queries.tsv` (one narrow query per block; aim for 20–200 hits each; more than 500 → add filters, fewer than 10 → broaden).
- **Gold set**: 5–10 papers the search must find. If a gold paper is missing from the candidates, the queries are wrong; fix them before reading.
- **Seed list**: the lab's own reference library, if one exists. Record what it lacks.

## 2. Search (free sources; only public terms leave the machine)

| Source | Use | Command |
|---|---|---|
| PubMed E-utilities | backbone; ≤ 3 requests/s, run one at a time | `scripts/pubmed.py search / fetch --abstract / cites / verify` |
| Europe PMC | preprints (`--preprints`), full-text search (`METHODS:"tool"`), forward and backward citations | `scripts/epmc.py search / citing / refs` |
| iCite | field-normalised citation ratio; ordering only | `scripts/epmc.py icite` |
| bioRxiv | has a preprint been published? | `scripts/epmc.py published <doi>` |
| Crossref | DOI metadata, retraction notices (`update-to`) | `vendor/k-dense/paper-lookup/references/crossref.md` |
| OpenAlex, Semantic Scholar | optional; small anonymous quotas, frequent 429 | `vendor/k-dense/paper-lookup` |

Not used: Google Scholar scraping, Sci-Hub or any unlicensed full text, Unpaywall without the user's consent (it needs an email address).

`jf field scan <slug>` runs every query and ranks candidates by how many queries found them.

## 3. Screen, then snowball

- Screen on **topic match first**; citation counts order the reading, they never decide inclusion. Keep small or negative studies that bear on a claim.
- Then snowball **from included papers only**: forward (`epmc.py citing <pmid> --terms …`) and backward (`refs`). Stop after two rounds that each add fewer than 5% new papers; if you stop for time, say the scan is not closed.
- Always run a preprint pass for the last 18 months, and map each preprint to its published version (keep the published one).
- Papers in parallel can be read by agents; give each a theme, the card schema, and the rule that findings come from the fetched abstract or full text, never from memory.

## 4. One card per paper (`templates/paper_card.json` → `raw/*.jsonl`)

Fields: identifiers · type (primary, method, resource, review, preprint) · modality · cohort · question · findings (with numbers) · validation shown · themes · relevance to our paper · `read_depth` · `verified`.

Rules:
- `read_depth: abstract` cannot support exact numbers from the body, methods details, or "they did not do X".
- Record what the data support, and separately any stronger claim the authors make. "May" is not "does"; "causes" only for designs that test cause.
- Do not repeat "first", "novel" or "state of the art" because the authors say so.
- For the 5–10 closest papers, read the full text (legal copy only) with PaperLens or `vendor/nature-skills/nature-paper-card`: story by figure, cohort, exact methods, what reviewers attacked (peer-review files when published).
- An API failure means "unverified", not "does not exist".

`jf field merge <slug>` deduplicates into `papers.jsonl`; `jf field verify <slug>` checks every PMID, title and year.

## 5. Synthesis (`field_map.md`; group by theme, never paper by paper)

1. **Timeline**: 12–20 turning points, one line each (what changed).
2. **Settled**: consensus statements, each with 1–3 citations.
3. **Contested or recently changed**: both sides, with the likely reason (cohort, platform, definition).
4. **Open questions** with stable ids (Q1, Q2 …) so the paper plan can point at them.
5. **Schemes table**: every published classification the paper must be compared with (states, niches, programmes), how each was defined.
6. **The bar**: closest papers × journal × cohort × technology × validation × functional work.
7. **Where our paper sits**: for each planned claim → new · extends · already shown · contradicted, with the papers; which "first" statements survive.
8. **Threats**: competing preprints, with dates.
9. **Missing from the lab's library.**
10. **Search record**: queries, dates, hit counts, what was not covered.

`jf field html <slug>` builds a browsable page (timeline, filters by theme, type and validation).

## 6. Use and refresh

- Stage 2 takes the bar table; stage 3 takes open questions and claim status; stage 5 takes consensus statements for the Introduction and contested points for the Discussion.
- Refresh before submission and at revision: rerun `jf field scan`; rows with `in_map = no` are what is new. Preprint servers move monthly in fast fields.
- Keep a reading log (`reading_log.md`): date, what was read at what depth, what changed in the map.
