# Stage 2 · Choosing the journal

1. **Type of paper first.** Mechanism (a principle shown by perturbation), atlas/resource (scale + reuse), technology (benchmark + one application), clinical (outcome in cohorts). The same data can be cut more than one way; say which cut each journal wants.
2. **Comparators.** From the field scan take the 5–10 closest papers of the last three years: journal, cohort size, modalities, orthogonal validation, replication, functional work. This table is the real bar; adjust `journals/<id>.json → bar` to it.
3. **Score and fit.** `jf fit projects/<p>/paper.json`. "fits" = no dimension short; "reach" = short by ≤ 2 points in total; "not yet" = more.
4. **Scenarios, not one answer.** For each scenario give: journal tier, the extra work, its cost in months, and the risk (competing preprints, scooping).
5. **Recommend** a target, a fallback inside the same publisher (transfer keeps reviews: Cell → Cancer Cell → Cell Reports Medicine; Nature → Nature Cancer / Genetics → Nature Communications), and a decision date.
6. **Pre-submission enquiry** when the fit is uncertain: Summary + one figure + why now; Cell and Nature both take them.
7. Things that move a paper up a tier, in the usual order of value per month: same-tissue orthogonal validation · replication of the main claim in an independent cohort · one perturbation that tests the nominated mechanism · a pre-specified clinical association · a usable resource (portal, model, code).
8. Things that do not: more clustering, more correlative panels, survival curves searched over many cut-offs.
