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

TXT_OUT = OUT_DIR / "sensitivity_analysis.txt"
CSV_OUT = OUT_DIR / "sensitivity_summary.csv"

DEFAULT_FAILING = 150
DEFAULT_EXCELLENT = 210

# ---------- helpers ----------
def add_derived(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["total_score"]   = df["math score"] + df["reading score"] + df["writing score"]
    df["average_score"] = df["total_score"] / 3
    return df

def categorize(total: float, failing_cutoff: int, excellent_cutoff: int) -> str:
    if total < failing_cutoff:
        return "Failing"
    elif total < excellent_cutoff:
        return "Average"
    else:
        return "Excellent"

def apply_categories(df: pd.DataFrame, failing_cutoff: int, excellent_cutoff: int) -> pd.DataFrame:
    df = df.copy()
    df["performance_category"] = df["total_score"].apply(
        lambda t: categorize(t, failing_cutoff, excellent_cutoff)
    )
    return df

def rates_by_category(df: pd.DataFrame, group_col: str = None) -> pd.DataFrame:
    if group_col is None:
        counts = df["performance_category"].value_counts().reindex(
            ["Excellent", "Average", "Failing"], fill_value=0
        )
        total = counts.sum()
        out = pd.DataFrame({
            "category": counts.index,
            "rate": counts.values / total
        })
        out.insert(0, "group", "OVERALL")
        return out
    else:
        pv = df.pivot_table(
            index=group_col,
            columns="performance_category",
            values="total_score",
            aggfunc="count"
        ).fillna(0)
        for col in ["Excellent", "Average", "Failing"]:
            if col not in pv.columns:
                pv[col] = 0
        pv["total"] = pv.sum(axis=1)
        out = pd.DataFrame({
            "group": pv.index.astype(str),
            "rate_excellent": pv["Excellent"] / pv["total"],
            "rate_average":   pv["Average"]   / pv["total"],
            "rate_failing":   pv["Failing"]   / pv["total"],
        }).reset_index(drop=True)
        return out

def disparate_impact_to_max(rate_series: pd.Series) -> pd.Series:
    m = rate_series.max()
    return rate_series / m if m > 0 else pd.Series(1.0, index=rate_series.index)

def compute_metrics(df: pd.DataFrame, failing_cutoff: int, excellent_cutoff: int, label: str) -> dict:
    d = add_derived(df)
    d = apply_categories(d, failing_cutoff, excellent_cutoff)

    metrics = {
        "scenario": label,
        "n": len(d),
        "mean_math": d["math score"].mean(),
        "mean_reading": d["reading score"].mean(),
        "mean_writing": d["writing score"].mean(),
        "mean_total": d["total_score"].mean(),
        "failing_cutoff": failing_cutoff,
        "excellent_cutoff": excellent_cutoff,
    }

    # Overall category rates
    overall_rates = rates_by_category(d, None).set_index("category")["rate"].to_dict()
    metrics.update({
        "rate_overall_excellent": overall_rates.get("Excellent", 0.0),
        "rate_overall_average":   overall_rates.get("Average", 0.0),
        "rate_overall_failing":   overall_rates.get("Failing", 0.0),
    })

    # Subgroup rates & DI
    by_gender = rates_by_category(d, "gender").set_index("group")
    by_race   = rates_by_category(d, "race/ethnicity").set_index("group")

    di_gender = disparate_impact_to_max(by_gender["rate_excellent"])
    di_race   = disparate_impact_to_max(by_race["rate_excellent"])

    metrics["min_DI_gender"] = di_gender.min()
    metrics["min_DI_race"]   = di_race.min()

    metrics["_tables"] = {
        "by_gender": by_gender.reset_index(),
        "by_race": by_race.reset_index(),
    }
    return metrics

def format_pct(x: float) -> str:
    return f"{100*x:.1f}%"

# ---------- load baseline data ----------
df_raw = pd.read_csv(DATA_FILE)
df_raw = add_derived(df_raw)

# ---------- scenarios ----------
scenarios = [
    ("baseline", df_raw.copy(), DEFAULT_FAILING, DEFAULT_EXCELLENT, "Full dataset; cutoffs = Failing<150, Excellent≥210"),
    ("remove_top_5pct", df_raw[df_raw["total_score"] <= df_raw["total_score"].quantile(0.95)].copy(),
        DEFAULT_FAILING, DEFAULT_EXCELLENT, "Removed top 5% total_score"),
    ("remove_bottom_5pct", df_raw[df_raw["total_score"] >= df_raw["total_score"].quantile(0.05)].copy(),
        DEFAULT_FAILING, DEFAULT_EXCELLENT, "Removed bottom 5% total_score"),
    ("excellent_220", df_raw.copy(), DEFAULT_FAILING, 220, "Threshold shift: Excellent≥220 (stricter)"),
    ("excellent_200", df_raw.copy(), DEFAULT_FAILING, 200, "Threshold shift: Excellent≥200 (lenient)")
]

# ---------- compute ----------
all_metrics = []
for label, df_s, fail_c, exc_c, desc in scenarios:
    m = compute_metrics(df_s, fail_c, exc_c, label)
    m["description"] = desc
    all_metrics.append(m)

# ---------- CSV summary ----------
rows = []
for m in all_metrics:
    rows.append({
        "scenario": m["scenario"],
        "description": m["description"],
        "n": m["n"],
        "failing_cutoff": m["failing_cutoff"],
        "excellent_cutoff": m["excellent_cutoff"],
        "mean_math": round(m["mean_math"], 3),
        "mean_reading": round(m["mean_reading"], 3),
        "mean_writing": round(m["mean_writing"], 3),
        "mean_total": round(m["mean_total"], 3),
        "rate_overall_excellent": round(m["rate_overall_excellent"], 4),
        "rate_overall_average": round(m["rate_overall_average"], 4),
        "rate_overall_failing": round(m["rate_overall_failing"], 4),
        "min_DI_gender": round(m["min_DI_gender"], 4),
        "min_DI_race": round(m["min_DI_race"], 4),
    })
pd.DataFrame(rows).to_csv(CSV_OUT, index=False)

# ---------- human-readable TXT ----------
lines = []
lines.append("===== SENSITIVITY / ROBUSTNESS ANALYSIS =====\n")
lines.append("Scenarios compared:")
for r in rows:
    lines.append(f"- {r['scenario']}: {r['description']} (n={r['n']})")
lines.append("")

baseline = next(m for m in all_metrics if m["scenario"] == "baseline")

def delta_str(b, x):
    d = x - b
    sign = "+" if d >= 0 else "-"
    return f"{sign}{abs(d):.3f}"

for m in all_metrics:
    lines.append(f"--- Scenario: {m['scenario']} ---")
    lines.append(f"Description: {m['description']}")
    lines.append(f"Rows: {m['n']}, Cutoffs: Failing<{m['failing_cutoff']}, Excellent≥{m['excellent_cutoff']}")
    lines.append(f"Means -> math:{m['mean_math']:.2f}  reading:{m['mean_reading']:.2f}  writing:{m['mean_writing']:.2f}  total:{m['mean_total']:.2f}")

    lines.append("Overall category rates:")
    lines.append(f"  Excellent: {format_pct(m['rate_overall_excellent'])} (Δ vs baseline {delta_str(baseline['rate_overall_excellent'], m['rate_overall_excellent'])})")
    lines.append(f"  Average:   {format_pct(m['rate_overall_average'])} (Δ vs baseline {delta_str(baseline['rate_overall_average'], m['rate_overall_average'])})")
    lines.append(f"  Failing:   {format_pct(m['rate_overall_failing'])} (Δ vs baseline {delta_str(baseline['rate_overall_failing'], m['rate_overall_failing'])})")

    lines.append("Fairness (Disparate Impact min across subgroups):")
    lines.append(f"  Gender DI min: {m['min_DI_gender']:.3f} (flag if < 0.80)")
    lines.append(f"  Race   DI min: {m['min_DI_race']:.3f} (flag if < 0.80)")

    lines.append("\n  By gender (rate_excellent, rate_average, rate_failing):")
    gtab = m["_tables"]["by_gender"][["group","rate_excellent","rate_average","rate_failing"]]
    for _, r in gtab.iterrows():
        lines.append(f"    {r['group']:<10}  Exc:{r['rate_excellent']:.3f}  Avg:{r['rate_average']:.3f}  Fail:{r['rate_failing']:.3f}")

    lines.append("\n  By race/ethnicity (rate_excellent, rate_average, rate_failing):")
    rtab = m["_tables"]["by_race"][["group","rate_excellent","rate_average","rate_failing"]]
    for _, r in rtab.iterrows():
        lines.append(f"    {r['group']:<10}  Exc:{r['rate_excellent']:.3f}  Avg:{r['rate_average']:.3f}  Fail:{r['rate_failing']:.3f}")
    lines.append("\n")

lines.append("===== INTERPRETATION HINTS =====")
lines.append("- If conclusions remain stable across scenarios, recommendations are robust.")
lines.append("- If Excellent rate or fairness DI swings a lot under small changes, flag as medium/high-risk.")
lines.append("- Use the CSV summary for tables in the stakeholder report.")

with open(TXT_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote sensitivity text report to: {TXT_OUT}")
print(f"✅ Wrote sensitivity summary CSV to: {CSV_OUT}")

log_run("sensitivity_analysis.py")        