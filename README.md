# Lab 2 - Decision Tree Modeling and Improvement

A decision tree baseline plus three improvement methods on the UCI
**Predict Students' Dropout and Academic Success** dataset: cost-complexity
pruning, class-imbalance handling, and dropping semester-outcome features
for early-warning prediction.

> Full repository (including `figures/`, `docs/`, commit history):
> <https://github.com/thphuc06/Lab2_DecisionTree>

## Repository structure

```text
data/raw/       Raw dataset (data.csv)
src/            Shared code: data loading/splitting, evaluation, plotting
notebooks/      6 notebooks: EDA, baseline, three improvements, comparison
figures/        Decision tree plots, confusion matrices, comparison charts
outputs/        Metrics (results.csv), classification reports, tree rules
docs/           Original assignment and the team's technical specs
docs/report/    Final PDF report submitted for the course
```

## How to run

1. Create a virtual environment and install dependencies (Python 3.11+):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
   ```

   `requirements-lock.txt` pins the exact package versions this project was
   built and verified with; notebooks `04` and `05` check these versions at
   the top and stop with an error if they don't match. `requirements.txt`
   only lists the direct dependencies by name (no pinned versions) and is
   kept for reference — installing from it can pull newer library versions
   that fail that check.

2. Run the six notebooks in `notebooks/` in order, `01` through `06`
   (open with Jupyter/VS Code and "Run All"). Every notebook calls
   `src/data.py::get_train_test()` for the same train/test split; none of
   them load or split the data on their own.

   Make sure each notebook's kernel points to the `.venv` created above
   (VS Code: "Select Kernel" -> Python Environments -> `.venv`), otherwise
   it will run on a different Python and fail to import the packages
   installed in step 1.

After running, `outputs/results.csv` will have five result rows (M0-M3),
and `figures/` will contain the decision tree plots, confusion matrices,
and comparison chart.

## Summary of results

| Model | Configuration | Test accuracy | Error rate |
| --- | --- | ---: | ---: |
| M0 | Baseline, unrestricted | 0.669 | 0.331 |
| M1 | Cost-complexity pruning | 0.756 | 0.244 |
| M2a | `class_weight="balanced"` | 0.651 | 0.349 |
| M2b | SMOTE (train set only) | 0.688 | 0.312 |
| M3 | Early-warning (12 semester features dropped) | 0.541 | 0.459 |

Detailed analysis and the reasoning behind each improvement are in the PDF
report (`docs/report/2 - Report.pdf`).

## Reference material in this repo

- [`docs/00-DE-BAI-GOC.pdf`](docs/00-DE-BAI-GOC.pdf): the original
  assignment brief.
- [`docs/02-DATASET-VA-CONG-VIEC.md`](docs/02-DATASET-VA-CONG-VIEC.md):
  dataset spec, preprocessing, and the five model configurations.
- [`AGENT.md`](AGENT.md): the team's working conventions and role split.

## Dataset

**Predict Students' Dropout and Academic Success** (UCI ML Repository,
id=697), released under CC BY 4.0.
