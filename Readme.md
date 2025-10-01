# Task 07 – Decision Making & Stakeholder Report

This repository contains the work for **Research Task 07: Ethical Implications of Decision Making**.  
It builds on Task 05 (Descriptive Statistics) and Task 06 (Deep Fake Interview) to create a **stakeholder-facing decision report** grounded in reproducible analysis, uncertainty quantification, fairness checks, and ethical/legal considerations.

---

## 📌 Purpose

The goal of Task 07 is to:
- Start from the narrative generated in prior tasks.
- Produce a clear, actionable report for human stakeholders.
- Document the entire process (code, prompts, outputs) for transparency and reproducibility.
- Emphasize **uncertainty**, **bias/fairness**, and **ethics** in decision-making.

---

## 📂 Repository Structure

```
Task07/
├─ data/
│  ├─ StudentsPerformance.csv          # Raw dataset (1,000 anonymized records)
│  └─ data_lineage.md                  # Data provenance and lineage
├─ scripts/
│  ├─ descriptive_stats.py             # Baseline stats, correlations
│  ├─ uncertainty_bootstrap.py         # Bootstrap confidence intervals
│  ├─ sanity_checks.py                 # Missingness, duplicates, outliers
│  ├─ bias_fairness.py                 # Fairness metrics, disparate impact
│  ├─ sensitivity_analysis.py          # Robustness to perturbations
│  └─ visuals.py                       # Generates figures for report
├─ outputs/
│  ├─ descriptive_stats.txt
│  ├─ uncertainty_cis.csv
│  ├─ sanity_checks.txt
│  ├─ fairness_summary.txt
│  ├─ fairness_metrics.csv
│  ├─ sensitivity_analysis.txt
│  ├─ sensitivity_summary.csv
│  └─ logs/
│     └─ run.log                       # Execution log with seeds & timestamps
├─ prompts/
│  ├─ llm_outputs_raw.md               # Raw LLM transcripts (Claude)
│  └─ llm_outputs_annotated.md         # Annotated edits & validation notes
├─ report/
│  ├─ Stakeholder_Report.md            # Final stakeholder-facing report
│  └─ figures/
│     ├─ hist_math_score.png
│     ├─ hist_reading_score.png
│     ├─ hist_writing_score.png
│     ├─ box_total_by_gender.png
│     └─ bar_performance_category.png
└─ README.md                           # (this file)
```

---

## ⚙️ How to Run

### Requirements
```bash
pip install pandas numpy matplotlib
```

### Steps
Run each script in order:

```bash
python scripts/descriptive_stats.py
python scripts/uncertainty_bootstrap.py
python scripts/sanity_checks.py
python scripts/bias_fairness.py
python scripts/sensitivity_analysis.py
python scripts/visuals.py
```

- Outputs will be saved to `outputs/`
- Figures will be saved to `report/figures/`
- Execution metadata (seed, timestamp, script) is logged in `outputs/logs/run.log`

---

## 📊 Report Structure (Stakeholder_Report.md)

The report follows the Task 07 prompt requirements:

1. **Title & purpose**
2. **Executive Summary (≤300 words)** – risk-tiered recommendations, uncertainty statement, one-sentence action
3. **Background & decision question**
4. **Data & methods (brief)**
5. **Findings (with visualizations & uncertainty)**
6. **Recommendations (tiered: low/medium/high risk)**
7. **Ethical & legal concerns**
8. **Next steps & validation plan**
9. **Appendices** – raw LLM outputs, annotated edits, scripts, data lineage

LLM-generated text is **explicitly labeled** in the report, and full transcripts are included in `prompts/`.

---

## 🔒 Ethical & Legal Notes

- Dataset: **Kaggle StudentsPerformance** (anonymized; no PII).  
- Potential ethical risks: fairness across subgroups, limitations in using synthetic LLM outputs, bias in recommendations.  
- Legal concerns: none for this dataset; flagged for awareness in broader applications.


---

## 👩‍💻 Authors

Prepared as part of Syracuse University Research Analyst work, Task 07.  
This work builds on **Task 05** (descriptive stats) and **Task 06** (deep fake audio narrative).
