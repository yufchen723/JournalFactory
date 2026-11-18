# Stage 0 · Inventory

Goal: one table of what exists, how solid it is, and where it lives. Everything later reads from it.

1. Walk the project folders (READMEs, reports, ledgers first; then results). Use read-only search agents for large trees; never write into another person's folder.
2. For each result record: claim in one line · key number · replicate unit and n · validation it has (none / external data / same tissue / functional) · path · status (final, exploratory, negative, superseded).
3. Keep negative and null results. They decide what the paper may claim.
4. Note what is absent: clinical table, orthogonal imaging, replication cohort, perturbation, deposited data.
5. Score the eight dimensions (0–3, `journals/_dimensions.json`) and write `projects/<p>/paper.json` with scenarios: as it is; plus analysis only; plus new data.
6. Sensitive files (patient identifiers) are listed by path only; never copied or summarised with identifiers.
