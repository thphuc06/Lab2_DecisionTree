# LaTeX report skeleton

This folder holds the actual written-report deliverable required by the
assignment (`docs/00-DE-BAI-GOC.pdf`, Section 3.3 "Written Report" /
Section 3.4 "Written Report Structure"), as a LaTeX project instead of a
shared Google Doc. It replaces the plan in `docs/02-DATASET-VA-CONG-VIEC.md`
Phần E1 ("Tạo Google Doc chung cho báo cáo") — the team decided a
git-based LaTeX skeleton fits this project's existing workflow better,
since everyone already edits files and commits per their own role.

## Structure

```
docs/report/
├── report.tex              master file -- \input's every section, in order
├── references.bib          shared bibliography (BibTeX), append-only
├── README.md                this file
└── sections/
    ├── a_group_intro.tex     Team lead   -- names, IDs, contributions
    ├── b_introduction.tex    Role A      -- FILLED IN, translated + fact-checked
    ├── c_dataset.tex         Role A      -- FILLED IN, translated + fact-checked
    ├── d_baseline.tex        Role B      -- skeleton only, needs translation
    ├── e_analysis.tex        Role B      -- skeleton only, needs translation
    ├── f1_pruning.tex        Role C      -- FILLED IN, translated + fact-checked
    ├── f2_imbalance.tex      Role D      -- skeleton only, needs translation
    ├── f3_features.tex       Role E      -- skeleton only, needs translation
    ├── g_comparison.tex      Role A      -- FILLED IN, translated + fact-checked
    └── h_conclusion.tex      Role A      -- FILLED IN, translated + fact-checked
```

Section i (References) is not a separate file -- it is generated
automatically from `references.bib` via `\bibliography{references}` at
the end of `report.tex`.

## Ownership -- same rule as the rest of the repo

One file, one owner, exactly like `docs/03-GIT-WORKFLOW-VA-CAU-TRUC-CODE.md`
already establishes for `src/`, `notebooks/`, and `progress/`. Edit only
the section file(s) listed as yours above. `references.bib` is the one
shared/append-only file (like `outputs/results.csv`): add a new `@entry`
at the bottom when you cite something new, never delete or rewrite
someone else's entry. `report.tex` itself rarely needs editing once every
section file exists -- treat it as team-lead/Role A territory.

## What "FILLED IN" vs "skeleton only" means

Role A's four sections (b, c, g, h) already contain full English content,
translated from the fact-checked Vietnamese drafts
(`docs/report_draft_b_c.md`, `docs/report_draft_g_h.md`) after the
2026-08-30 audits that found and fixed multiple real errors (wrong
correlation values, incomplete tree rules, and model-comparison mix-ups --
see `progress/A.md` for the full audit trail). Nothing in those four files
was invented for this skeleton.

Role C's `f1_pruning.tex` has since been completed from its independently
verified source draft and rerun notebook; it contains no `\todo` placeholder.

The remaining five sections (a, d, e, f2, f3) are **structural skeletons
only**: correct `\section`/`\subsection` headers matching the assignment's
exact wording, `\includegraphics` calls already pointing at the right,
already-committed figure files, and `\todo{...}` placeholders (rendered
in red in the compiled PDF) describing exactly what needs to go there and
which already-verified source file to translate/adapt from. Each source
draft was independently audited on 2026-08-30 (see `progress/A.md`):
B (`docs/report_draft_d_e.md`), C (`docs/report_draft_f1_pruning.md`), and
E (`notebooks/05_improve_features.ipynb`) came back with **zero errors**;
D (`docs/report_draft_f2_imbalance.md`) had 2 small wording errors, already
fixed. Owners of unfinished sections should adapt the corresponding verified
source rather than re-derive numbers from scratch -- the values were already
checked against primary result files (`outputs/results.csv`, classification
reports, etc.), and re-deriving them risks reintroducing a caught error.

Search for `\todo` in a section file (or look for red text in the
compiled PDF) to find everything still missing in that file.

## Style rule: keep figure captions short, put analysis in body text

`\caption{...}` should describe what the figure shows in one short
sentence -- axes, what's being compared, nothing more. Do not put
interpretation, numbers, or "why this matters" reasoning inside a
`\caption{}`; write that as a normal paragraph immediately before or
after the `\begin{figure}...\end{figure}` block instead. This was fixed
across `c_dataset.tex` and `g_comparison.tex` on 2026-08-30 after
captions had grown into multi-sentence analysis paragraphs -- follow the
pattern already used in those files and in `f1_pruning.tex` (short caption,
then a paragraph of real prose right after the figure) when filling in
`d_baseline.tex`, `e_analysis.tex`, `f2_imbalance.tex`, and
`f3_features.tex`.

## How to compile

You need a LaTeX distribution (TeX Live, MiKTeX, or Overleaf).
`report.pdf` is the current 27-page A4 preview tracked with this source. It
was compiled with MiKTeX 26.5 and rendered page by page during the final
2026-08-30 integration audit: the LaTeX log has no errors, undefined
citations/references, rerun requests, or overfull boxes. This establishes
that the report framework and every referenced figure are technically
healthy; it is still a **skeleton preview, not a submission-ready report**,
because the five remaining owner sections listed above intentionally retain
red `\todo{...}` placeholders. Recompile whenever any `.tex`, `.bib`, or
referenced figure changes; do not treat an older PDF timestamp as evidence
that the source still compiles.

```bash
cd docs/report
pdflatex report.tex
bibtex report
pdflatex report.tex
pdflatex report.tex   # run twice after bibtex so citation numbers settle
```

Or open `docs/report/` as an Overleaf project (upload the folder, or
connect the GitHub repo) -- Overleaf compiles automatically and needs no
local install, which may be the easier option for teammates without
LaTeX set up locally.

## Before final submission

- Search the whole `sections/` folder for `\todo` and make sure none
  remain (`rg -n '\\todo' sections`).
- Compile once from a clean checkout to make sure nothing depends on a
  local file outside this repo.
- Cross-check every number against `outputs/results.csv` /
  `outputs/comparison_table.csv` one more time -- copy-paste or
  translation mistakes are easy to introduce even from a verified
  source. This is exactly the kind of check that already caught 5 errors
  in the Vietnamese drafts; do not assume translation is risk-free.
- Export the final PDF (`report.pdf`) and rename it per the submission
  convention in the brief: `[GroupID - Report].pdf`.
