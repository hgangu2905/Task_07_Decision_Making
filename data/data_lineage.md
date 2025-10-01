# Data Lineage (Task 07)

## Source
- Kaggle StudentsPerformance dataset (`StudentsPerformance.csv`).
- 1,000 anonymized student records with demographics, parental education, lunch type, test prep status, and math/reading/writing scores.

## Transformations
1. **Raw load** – CSV imported via Pandas (`descriptive_stats.py`, `uncertainty_bootstrap.py`, etc.).
2. **Derived fields**:
   - `total_score = math + reading + writing`
   - `average_score = total_score / 3`
   - `performance_category`:
     - Failing (<150)
     - Average (150–209)
     - Excellent (≥210)
3. **Validation checks** (`sanity_checks.py`):
   - Verified no missing/duplicate values.
   - Scores constrained between 0–100.
   - Outliers flagged but not dropped.
4. **Analysis modules**:
   - Descriptive statistics → `outputs/descriptive_stats.txt`
   - Bootstrap uncertainty → `outputs/uncertainty_cis.csv`
   - Fairness metrics → `outputs/fairness_summary.txt`
   - Sensitivity/robustness → `outputs/sensitivity_analysis.txt`, `outputs/sensitivity_summary.csv`
   - Visualizations → `report/figures/*.png`

## Outputs
- All outputs stored in `outputs/` (text + CSV).
- Figures stored in `report/figures/`.
- Final synthesis in `report/Stakeholder_Report.md`.

