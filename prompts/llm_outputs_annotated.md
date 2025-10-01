# Annotated LLM Outputs (Task 7)

This file explains how the raw LLM outputs were **used, modified, or discarded** during Task 7.  

---

## What Was Kept  

- **Basic dataset facts** (1,000 students, score ranges 0–100, demographics included).  
- **Averages** (math ≈66, reading ≈69, writing ≈68) – verified against scripts.  
- **Impact of test preparation** – improvement patterns consistent with analysis.  
- **Parental education ranking** – Master's > Bachelor's > Associate > others, consistent with script outputs.  

---

## What Was Modified  

- **Performance categories:**  
  - Claude used *Low/Average/High/Excellent*.  
  - We standardized to **Failing/Average/Excellent** per Task definition.  

- **Counts of Excellent students:**  
  - Claude’s numbers differed due to alternate thresholds.  
  - Our scripts recalculated using consistent cutoffs (≥210 for Excellent).  

- **Wording:**  
  - Claude’s narrative suggestions were rephrased into concise, neutral stakeholder language.  

---

## What Was Discarded  

- **Interactive artifacts** (visual demos) – not reproducible in this repo.  
- **Speculative interpretations** not supported by data.  

---

## Validation  

Every number in the final Stakeholder Report was **cross-checked** with:  
- Descriptive stats (`descriptive_stats.py`)  
- Bootstrap uncertainty (`uncertainty_bootstrap.py`)  
- Fairness analysis (`bias_fairness.py`)  
- Sensitivity tests (`sensitivity_analysis.py`)  

