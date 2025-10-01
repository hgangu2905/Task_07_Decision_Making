# Stakeholder Report: Student Performance Dataset  
*Task 7 – Research Analyst Project*  

---
> **Note:** The Stakeholder Report was drafted with assistance from a large language model (see `prompts/llm_outputs_raw.md`). All claims were validated against the analysis outputs in `outputs/`.
---

## Stakeholders & Decision Context  

The primary stakeholders are:  
- **School administrators and curriculum planners** – responsible for allocating resources such as tutoring programs and test preparation courses.  
- **Equity and compliance officers** – tasked with ensuring fairness across gender and race/ethnicity groups.  
- **Teachers and academic support staff** – directly implementing interventions for underperforming students.  

**Decision faced:**  
Stakeholders must decide how to prioritize interventions (e.g., whether to target Average students broadly, focus on subgroup disparities, or intensify test preparation programs) while balancing performance gains with fairness and ethical obligations.  

---

## Executive Summary  

This report analyzes the *Student Performance Dataset* (1,000 records) to inform evidence-based educational decisions. The dataset includes demographics, test preparation, and scores in math, reading, and writing.  

**Key findings:**  
- **Average performance:** Students scored ~66 in math, ~69 in reading, and ~68 in writing, with an average total of ~203.  
- **Uncertainty:** Bootstrap 95% confidence intervals show the average total score is highly stable, between **200.7 and 205.9**.  
- **Group disparities:** Females slightly outperform males (Cohen’s d = 0.26). Race/ethnicity group E has the highest Excellent rate (62%), while groups A, B, and C show disparate impacts (<0.80 threshold).  
- **Sanity checks:** No missing data, duplicates, or invalid values detected. Outliers exist but do not distort overall conclusions.  
- **Robustness:** Sensitivity analysis (±5% trimming and threshold shifts) confirms that the main recommendation—focusing on students in the *Average* category—remains consistent across all tested conditions.  

**Recommendations (tiered):**  
- **Low risk:** Provide targeted support to students in the Average band (~40% of population).  
- **Medium risk:** Trial extended test preparation programs; effectiveness varies by subgroup.  
- **High risk:** Subgroup-specific interventions (e.g., by race/ethnicity) carry fairness risks and require careful ethical review.  

**Uncertainty Statement:**  
All numerical results are accompanied by bootstrap confidence intervals and robustness checks to quantify reliability.  

**One-Sentence Action Recommendation:**  
*Prioritize interventions for students in the Average band, as this remains the most stable and equitable target under all tested scenarios.*  

---

## Background & Methods  

The dataset (public Kaggle source) includes demographics, parental education, lunch type, test preparation course, and test scores.  

Scripts executed:  
- `descriptive_stats.py` – summary statistics & correlations.  
- `uncertainty_bootstrap.py` – bootstrap confidence intervals.  
- `sanity_checks.py` – missingness, duplicates, outliers.  
- `bias_fairness.py` – subgroup performance & disparate impact.  
- `sensitivity_analysis.py` – robustness to trimming and threshold shifts.  

Outputs are logged in the `outputs/` folder. Bootstrap seeds were fixed for reproducibility.  

### Data Provenance & Limitations  
- **Source:** Public Kaggle dataset (“StudentsPerformance.csv”), simulated educational records.  
- **Collector:** Kaggle community; not collected under controlled academic conditions.  
- **Limitations:** Secondary dataset, not representative of all student populations. Potential biases in sampling and feature definitions. Cannot be used for high-stakes policy decisions without external validation.  

### Data Lineage  
1. **Raw data**: CSV file in `data/StudentsPerformance.csv`.  
2. **Processing scripts**: Python scripts in `scripts/` generated derived fields (`total_score`, `average_score`, `performance_category`).  
3. **Outputs**: Stored in `outputs/` (TXT and CSV summaries).  
4. **Report**: Findings synthesized into this stakeholder report.  

---

## Findings  

### Descriptive Statistics  
- Dataset has **1,000 rows × 10 columns**; all values are valid, no missingness or duplicates.  
- Average scores: Math (66), Reading (69), Writing (68).  
- Strong correlation between reading and writing (r ≈ 0.87).  
- ~5% of students underperform with total score <150.  

### Uncertainty (Bootstrap CIs)  
- Math mean: 65.2–67.0  
- Reading mean: 68.3–70.1  
- Writing mean: 67.1–69.0  
- Total score mean: 200.7–205.9  
→ Confirms dataset averages are stable within ±2–3 points.  

### Sanity Checks  
- No missing or duplicate records.  
- Scores all within expected 0–100 range.  
- Outliers exist (detected by IQR), but do not distort distributions.  
- Balanced categorical distributions across gender, race/ethnicity, and parental education.  

### Fairness & Bias  
- Females outperform males slightly (Excellent rate = 51.7% vs 39.2%).  
- Cohen’s d (gender) = **0.26** (small-to-medium effect).  
- Race group E has the highest Excellent rate (62%); groups A, B, and C fall below disparate impact threshold (<0.8).  
- Disparate impact flags: Gender DI = 0.766, Race DI = 0.452.  

### Sensitivity & Robustness  
- Removing top/bottom 5% of total scores shifts means by <±6 points.  
- Adjusting Excellent cutoff (200 ↔ 220) changes category shares, but fairness gaps persist.  
- Across all scenarios, **focus on the Average group (~40–45% of students)** remains the most robust intervention target.  

### Figures 
- Score distributions: `report/figures/hist_math_score.png`, `report/figures/hist_reading_score.png`, `report/figures/hist_writing_score.png`  
- Total score by gender: `report/figures/box_total_by_gender.png`  
- Performance category distribution: `report/figures/bar_performance_category.png`


---

## Recommendations  

- **Low Risk:**  
  - Focus interventions on Average students (~40% of dataset).  
  - Continue using total score as a composite metric.  

- **Medium Risk:**  
  - Pilot extended test prep programs; early evidence suggests subgroup variability.  
  - Track longitudinal improvements with confidence intervals.  

- **High Risk:**  
  - Avoid subgroup-based resource allocation without external ethical/legal review.  
  - Monitor disparate impact for compliance with fairness standards.  

---

## Ethical & Legal Considerations  

- Dataset is anonymized and public; no PII.  
- Fairness gaps across gender and race/ethnicity highlight risks if subgroup-targeted decisions are made.  
- Human oversight is essential; automated allocation may amplify disparities.  
- Any policy changes should be reviewed under education equity frameworks.  

---

## Next Steps  

- Collect longitudinal performance data to validate causality.  
- Explore external datasets to triangulate subgroup disparities.  
- Implement fairness monitoring in future interventions.  
- Engage stakeholders (teachers, administrators, ethicists) before high-risk actions.  

---

## Appendices  

- **Outputs:** see `outputs/` folder.  
- **Scripts:** see `scripts/` folder.  
- **Prompts & LLM Outputs:** Raw LLM prompts/outputs were used in drafting but not retained in this repo. Instead, LLM assistance is disclosed in the Methods section, and all generated text was validated against descriptive statistics, uncertainty intervals, and fairness metrics.  
- **Data Lineage:** summarized in the Background & Methods section.  

---
