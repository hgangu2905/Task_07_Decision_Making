import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42  # set once for reproducibility
np.random.seed(SEED)

def log_run(script_name: str, note: str = ""):
    with open(LOG_DIR / "run.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {script_name} | seed={SEED} {note}\n")


# ---------- paths ----------
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA_FILE = ROOT / "data" / "StudentsPerformance.csv"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FAIRNESS_CSV = OUT_DIR / "fairness_metrics.csv"
SUMMARY_TXT  = OUT_DIR / "fairness_summary.txt"

# ---------- load & derive ----------
df = pd.read_csv(DATA_FILE)
df["total_score"]   = df["math score"] + df["reading score"] + df["writing score"]
df["average_score"] = df["total_score"] / 3

def categorize(total):
    if total < 150:
        return "Failing"
    elif total < 210:
        return "Average"
    else:
        return "Excellent"

df["performance_category"] = df["total_score"].apply(categorize)

# ---------- helpers ----------
def cohen_d(x, y):
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return np.nan
    s1, s2 = x.std(ddof=1), y.std(ddof=1)
    # pooled standard deviation
    sp = np.sqrt(((nx - 1) * s1**2 + (ny - 1) * s2**2) / (nx + ny - 2))
    if sp == 0:
        return 0.0
    return (x.mean() - y.mean()) / sp

def group_table(df, dimension):
    # counts
    grp = df.groupby(dimension, dropna=False)
    counts = grp.size().rename("count")
    mean_total = grp["total_score"].mean().rename("mean_total_score")

    # rates by category
    cat_counts = df.pivot_table(index=dimension, columns="performance_category",
                                values="total_score", aggfunc="count").fillna(0)
    for col in ["Excellent", "Average", "Failing"]:
        if col not in cat_counts.columns:
            cat_counts[col] = 0

    # convert to rates
    rates = cat_counts.div(counts, axis=0).rename(columns={
        "Excellent": "rate_excellent",
        "Average"  : "rate_average",
        "Failing"  : "rate_failing"
    })

    # disparate impact vs best subgroup (Excellent rate)
    max_rate = rates["rate_excellent"].max()
    if max_rate == 0:
        disp = pd.Series(1.0, index=rates.index, name="disparate_impact_vs_max_excellent")
    else:
        disp = (rates["rate_excellent"] / max_rate).rename("disparate_impact_vs_max_excellent")

    out = pd.concat([counts, mean_total, rates, disp], axis=1).reset_index()
    out.insert(0, "dimension", dimension)
    out = out.rename(columns={dimension: "subgroup"})
    return out

# ---------- compute fairness tables ----------
by_gender = group_table(df, "gender")
by_race   = group_table(df, "race/ethnicity")

fair_table = pd.concat([by_gender, by_race], ignore_index=True)
fair_table.to_csv(FAIRNESS_CSV, index=False)

# ---------- effect size for gender (total score) ----------
female_scores = df.loc[df["gender"] == "female", "total_score"]
male_scores   = df.loc[df["gender"] == "male", "total_score"]
d_gender = cohen_d(female_scores, male_scores)

# ---------- summary ----------
lines = []
lines.append("===== FAIRNESS SUMMARY =====")
lines.append(f"Rows analyzed: {len(df)}")
lines.append("")

def top_subgroup(tbl, dim):
    t = tbl[tbl["dimension"] == dim].copy()
    t = t.sort_values("rate_excellent", ascending=False)
    if len(t) == 0:
        return None
    return t.iloc[0].to_dict()

top_gender = top_subgroup(fair_table, "gender")
top_race   = top_subgroup(fair_table, "race/ethnicity")

if top_gender:
    lines.append(f"Top gender by Excellent rate: {top_gender['subgroup']} "
                 f"({top_gender['rate_excellent']:.3f})")
if top_race:
    lines.append(f"Top race/ethnicity by Excellent rate: {top_race['subgroup']} "
                 f"({top_race['rate_excellent']:.3f})")

lines.append("")
lines.append("Cohen's d (total_score, female vs male): "
             f"{d_gender:.3f} (positive means female > male)")

# disparate impact quick flags (common heuristic: < 0.8 can be concerning)
flags = fair_table.loc[fair_table["disparate_impact_vs_max_excellent"] < 0.8,
                       ["dimension", "subgroup", "disparate_impact_vs_max_excellent"]]
lines.append("")
lines.append("Subgroups with disparate impact < 0.80 (vs. best Excellent-rate subgroup):")
if len(flags) == 0:
    lines.append("None")
else:
    for _, r in flags.iterrows():
        lines.append(f"- {r['dimension']} = {r['subgroup']}: "
                     f"{r['disparate_impact_vs_max_excellent']:.3f}")

with open(SUMMARY_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote fairness table to: {FAIRNESS_CSV}")
print(f"✅ Wrote fairness summary to: {SUMMARY_TXT}")

log_run("bias_fairness.py")       