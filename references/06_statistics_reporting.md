# Stage 6 · Statistics and reporting

- Replicate unit is the patient (or section), never the pixel or cell. Pixel-level tests need a mixed model or per-patient summaries.
- State for each test: n, unit, test, sidedness, correction and the number of tests, effect size with interval.
- Survival: pre-specify the variable and cut-off; report continuous HR per SD; replicate in an independent cohort; a grid search over cut-offs is exploratory and must be reported as such.
- Spatial statistics: say the null (permutation within tissue), the neighbourhood size, and edge handling.
- Data and code: raw and processed data in a controlled-access or public archive (human sequence data usually dbGaP/EGA), code in a public repository with a DOI, accession numbers in the text.
- Human samples: IRB approval, consent, sex/age reporting, de-identified clinical table.
- Guides: `vendor/nature-skills/nature-statistics`, `vendor/cancer-cell-skills/skills/{cc-statistics,cc-reporting-standards}`, `vendor/cell-skills/skills/cell-data`.
