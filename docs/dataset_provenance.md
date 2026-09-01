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
  (recompute with
  `Get-FileHash -Algorithm SHA256 -LiteralPath data/raw/data.csv` on
  PowerShell or `sha256sum data/raw/data.csv` on macOS/Linux to confirm the
  file has not been altered since this note was written).
- Cross-checking the 36 CSV feature names against Table 1 of the companion
  paper (which lists 34 attributes) shows that `Previous qualification
  (grade)` and `Admission grade` are present in the CSV but absent from that
  table. The two source counts themselves are documentation claims mapped in
  the table below.

## From the dataset's published documentation, not independently verified

These facts are not recoverable from the CSV alone -- there is no column
that names the institution, the license, or the calendar years -- so the
group relies on the primary source documentation below. All web sources were
accessed on **2026-09-01**.

| External claim used by the report | Primary source and stable identifier | Exact source location | Report use |
|---|---|---|---|
| Dataset title, UCI ID 697, 4,424 instances, 36 features, three-class task | UCI Machine Learning Repository, <https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success>, DOI <https://doi.org/10.24432/C5MC89> | Page title; `Dataset Characteristics`; `Dataset Information` | `c_dataset.tex`, Data source and raw-shape discrepancy discussion (`realinho2021dataset`) |
| Dataset license is CC BY 4.0 | Same UCI record and DOI | `License` panel | `c_dataset.tex`, Data source (`realinho2021dataset`) |
| Enrollment-related fields and end-of-semester outcome families are both present | Same UCI record and DOI | Opening dataset description and `Dataset Information` | `c_dataset.tex`, Data source; motivates the conditional timing experiment in `f3_features.tex` |
| Numeric `Course` codes map to named programs, including 33 = Biofuel Production Technologies, 9119 = Informatics Engineering, 9238 = Social Service, and 9500 = Nursing | Same UCI record and DOI | `Variables Table`, row `Course` | Program names in `c_dataset.tex`; only counts/rates are computed from the local CSV |
| Records span academic years 2008/09--2018/19 and cover 17 undergraduate degrees; source systems and feature families | Realinho et al., *Data* 7(11):146 (2022), <https://www.mdpi.com/2306-5729/7/11/146>, DOI <https://doi.org/10.3390/data7110146> | Section 2, `Data Description`, especially the opening paragraphs before Table 1 | `c_dataset.tex`, Data source and ethical-note scope (`realinho2022predicting`) |
| Companion paper's attribute inventory contains 34 feature rows | Same paper and DOI | Table 1, `Description of the attributes in the dataset` | Compared with the local CSV/UCI count in `c_dataset.tex` |
| `Course` and `Tuition fees up to date` appear among the paper's leading permutation-importance variables | Same paper and DOI | Section 4, feature-importance discussion and corresponding importance figure/table | Comparative EDA interpretation in `c_dataset.tex` (`realinho2022predicting`) |

The institution name in the report is also supported by the UCI creators'
affiliations and the companion paper's author affiliation. The report uses the
English rendering **Instituto Politécnico de Portalegre** consistently with the
published sources; the CSV alone cannot establish that identity.

The UCI page describes certain inputs as known at enrollment, but the local
snapshot has no row-level timestamps and does not prove when mutable fields
(notably `Tuition fees up to date`) were captured. The M3 report section therefore
treats availability as an explicit study assumption and requires an institutional
data dictionary plus snapshot timestamps before any deployment claim.

## Why this distinction matters

During the final submission audit, the report was checked for numbers that
could not be traced to either a code artifact or an in-report
table/figure (see `AGENT.md`, "Mọi số liệu trong báo cáo phải truy được
nguồn"). The CSV-verifiable facts above meet that bar directly. The
documentation-sourced facts meet it through the cited references instead
-- they are still legitimate, but a reader should know which category a
given claim falls into if they want to reproduce it from the data alone.
