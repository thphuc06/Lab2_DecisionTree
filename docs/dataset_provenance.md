# Dataset provenance

This note separates what the group verified directly from the raw CSV
from what relies on the dataset's published documentation. Both are used
in the report (`docs/report/`), but they carry different levels of
certainty, and the report should not blur the two.

## Verified directly from `data/raw/data.csv`

The group inspected the raw file itself rather than trusting any
metadata page. These facts are reproducible by anyone who opens the CSV:

- 4,424 rows, 37 columns (36 features + `Target`).
- Zero missing values in any column.
- `Target` has exactly 3 classes: Graduate (2,209, 49.93%), Dropout
  (1,421, 32.12%), Enrolled (794, 17.95%).
- `Course` has 17 distinct codes.
- SHA256 checksum of the file as committed in this repo:
  `037b6403d6bf6f5d99b47c5375403ddbca9158f7ea367163499f973908e6604c`
  (recompute with `sha256sum data/raw/data.csv` to confirm the file has
  not been altered since this note was written).
- The UCI metadata page states 36 features, but Table 1 of the companion
  paper lists only 34; cross-checking against the actual column list, the
  discrepancy is exactly `Previous qualification (grade)` and
  `Admission grade`, present in the CSV but absent from the paper's
  table (see `docs/report/sections/c_dataset.tex`).

## From the dataset's published documentation, not independently verified

These facts are not recoverable from the CSV alone -- there is no column
that names the institution, the license, or the calendar years -- so the
group relies on the source documentation for them:

- Dataset: "Predict Students' Dropout and Academic Success", UCI Machine
  Learning Repository, id=697, DOI 10.24432/C5MC89 (cite key
  `realinho2021dataset` in `docs/report/references.bib`).
- Companion paper: Realinho et al., "Predicting Student Dropout and
  Academic Success", *Data* 7(11):146, 2022, DOI 10.3390/data7110146
  (cite key `realinho2022predicting` in `docs/report/references.bib`).
- License: CC BY 4.0, as stated on the UCI page.
- Institution and years: Instituto Politécnico de Portalegre, Portugal;
  academic years 2008/09 to 2018/19.
- Program names behind each numeric `Course` code (e.g. code 33 =
  Biofuel Production Technologies, code 9500 = Nursing) -- the raw CSV
  only contains the numeric codes; the name mapping comes from the UCI
  variable documentation.

## Why this distinction matters

The report was audited multiple times this session for numbers that
could not be traced to either a code artifact or an in-report
table/figure (see `AGENT.md`, "Mọi số liệu trong báo cáo phải truy được
nguồn"). The CSV-verifiable facts above meet that bar directly. The
documentation-sourced facts meet it through the cited references instead
-- they are still legitimate, but a reader should know which category a
given claim falls into if they want to reproduce it from the data alone.
