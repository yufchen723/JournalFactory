# Attack surface: typical objections by paper category

All of this file is **inference / craft guidance (not a journal rule)**. It lists objections that referees commonly raise, so the authors can meet them before submission. The only Cell text behind it is the criterion per article type (cell.md §2) and the required "Limitations of the study" subsection (cell.md §3).

For each objection: the trigger, what a referee writes, and the two ways to answer (evidence or scope).

## 1. Technology plus atlas papers

| Objection | Trigger | Answer with evidence | Answer with scope |
|---|---|---|---|
| "The method is incremental." | Benchmarks only against older or weaker methods | Head-to-head comparison on the same samples, with quantitative metrics and failure cases | State exactly which capability is new; drop general superiority claims |
| "Proof of principle is thin." | The biology section restates known anatomy or markers | One finding that could not have been made without the method, validated orthogonally | Submit as a Resource and say what the proof of principle is |
| "The atlas is descriptive." | Results are a tour of clusters and maps | A tested hypothesis that the atlas generated | Frame as a resource; make data access and reuse concrete |
| "Cell states or niches are over-split." | Many clusters, weak markers, one resolution | Stability across parameters, samples and an independent method | Merge; report only reproducible groups |
| "Not validated in tissue." | Computational calls only | Staining or an orthogonal assay on the same or matched tissue | Mark calls as predicted |
| "Sample size and diversity." | Few donors; one site; one platform | More samples, or mapping onto public cohorts | State the cohort limits in "Limitations of the study" |
| "Batch and technical confounds." | Conditions align with runs or slides | Design table; analysis showing the effect survives within batch | Report as a limit |
| "Data and code are not usable." | Accessions pending; code "on request" | Deposit before submission; reviewer access tokens | — (see `cell-data`) |

A technology-plus-atlas paper is attacked from both sides: method referees ask for benchmarks, biology referees ask for insight. Decide which claim leads and let the other support it.

## 2. Mechanism claims from correlative data

| Objection | Trigger | Answer with evidence | Answer with scope |
|---|---|---|---|
| "Correlation, not causation." | "drives", "regulates", "required for" on co-variation or co-localization | Loss and gain of function; rescue; temporal order | Association wording throughout, including title and Highlights |
| "Direction is not established." | A and B correlate | Perturb A, read B, and the reverse | State both directions as open |
| "Confounded by composition." | Bulk or spot-level signal that could reflect cell-type mix | Analysis within one cell type; deconvolution with validation | Describe as tissue-level association |
| "Inferred networks are predictions." | Regulatory or ligand–receptor inference presented as interaction | Perturbation of one or two top predictions; binding or reporter data | Call them predicted; rank by support |
| "Sufficiency is missing." | Only loss of function | Gain of function or reconstitution | Claim necessity only |
| "Specificity of the perturbation." | One guide, one inhibitor, one clone | Second reagent; rescue; dose response | — |
| "Alternative pathway not excluded." | A known parallel route exists | The experiment that separates them | Discuss it explicitly |

Wording ladder (weakest to strongest): is associated with → predicts → is consistent with a role in → is required for → is sufficient for → acts through. Each step up needs a new kind of evidence.

## 3. Single-cohort clinical association

| Objection | Trigger | Answer with evidence | Answer with scope |
|---|---|---|---|
| "No independent validation." | One cohort | Second cohort or public dataset; pre-specified analysis | Call it exploratory |
| "Small n, many variables." | Tens of patients, many features tested | Correction across all tests; effect sizes with intervals | Reduce to pre-specified hypotheses |
| "Cut-point chosen after the fact." | "High" and "low" groups from an optimised threshold | Median or pre-set threshold; continuous model | Report as hypothesis-generating |
| "Known prognostic factors ignored." | Univariate survival only | Multivariable model with the accepted clinical and molecular covariates of the disease | State which covariates were unavailable |
| "Treatment and sampling heterogeneity." | Mixed regimens, mixed sampling sites or times | Stratified or adjusted analysis | Restrict the claim to the homogeneous subgroup |
| "Selection bias." | Convenience samples | Flow diagram of inclusion; compare with the source population | Say so in limits |
| "Association is not a biomarker." | "Predictive" or "therapeutic target" language | Prospective or interventional data | Remove clinical-utility claims |

## 4. Model-system relevance

| Objection | Trigger | Answer with evidence | Answer with scope |
|---|---|---|---|
| "Cell lines do not reflect tissue." | Mechanism only in long-established lines | Primary cells, organoids or tissue; show the pathway is present in patient material | Limit the claim to the system |
| "Mouse is not human." | Species differences known for the pathway | Conservation of the key step in human samples | State as a limit |
| "Overexpression artefact." | Non-physiological levels | Endogenous tagging; knock-in; titration | — |
| "In vitro conditions drive the phenotype." | Medium, oxygen, matrix differ from tissue | Repeat under closer conditions or in vivo | Limit |
| "Human data are only correlative, model data only mechanistic." | The two halves never meet | One experiment that tests the human-derived prediction in the model, and one human readout of the model-derived mechanism | Make the bridge explicit in the Discussion |

## 5. Cross-cutting objections

- **Statistics**: wrong replicate unit, uncorrected multiple testing, undefined n (see `cell-statistics`).
- **Overclaiming**: title and Highlights stronger than the Results.
- **Prior work**: a close paper not cited or not distinguished. Verify before naming one (`cell-citation`).
- **Reproducibility**: representative images without counts; experiments shown once.
- **Limits not owned**: "Limitations of the study" is generic. cell.md §3 requires it to be specific to the paper.

## 6. Using this file

1. Assign the paper to one or more categories.
2. For each row whose trigger is present, write a major or minor point (format in `review-report-format.md`).
3. For each point, record both answers. Let the authors choose evidence or scope.
4. Do not raise a row whose trigger is absent.
