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

SUMMARY_TXT = OUT_DIR / "sanity_checks.txt"
OUTLIERS_CSV = OUT_DIR / "outliers_indices.csv"
CAT_COUNTS_CSV = OUT_DIR / "categorical_value_counts.csv"

# ---------- load & derive ----------
df = pd.read_csv(DATA_FILE)

# Derived columns (mirror your descriptive_stats.py)
df["total_score"]   = df["math score"] + df["reading score"] + df["writing score"]
df["average_score"] = df["total_score"] / 3

# ---------- helpers ----------
def iqr_outliers(series: pd.Series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (series < lower) | (series > upper)
    return mask, (lower, upper)

score_cols = ["math score", "reading score", "writing score", "total_score", "average_score"]

categorical_cols = [
    c for c in df.columns
    if c not in score_cols and df[c].dtype == "object"
]

# ---------- checks ----------
lines = []

# Shape & dtypes
lines.append("===== SHAPE & DTYPES =====")
lines.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
dtype_info = df.dtypes.to_string()
lines.append(dtype_info)
lines.append("")

# Missingness
lines.append("===== MISSINGNESS =====")
missing = df.isna().sum()
missing_pct = (missing / len(df) * 100).round(2)
miss_df = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
lines.append(miss_df.to_string())
lines.append("")

# Duplicates
lines.append("===== DUPLICATES =====")
dup_count = df.duplicated().sum()
lines.append(f"Duplicate rows: {dup_count}")
lines.append("")

# Score range validation (expected 0–100 for individual scores)
lines.append("===== SCORE RANGE VALIDATION (0-100) =====")
for col in ["math score", "reading score", "writing score"]:
    below = (df[col] < 0).sum()
    above = (df[col] > 100).sum()
    lines.append(f"{col}: below 0 = {below}, above 100 = {above}")
lines.append("")

# Descriptive stats quick view
lines.append("===== DESCRIPTIVE SUMMARY (SCORES) =====")
lines.append(df[score_cols].describe().to_string())
lines.append("")

# Correlations among scores
lines.append("===== CORRELATIONS (SCORES) =====")
lines.append(df[score_cols].corr().round(3).to_string())
lines.append("")

# Outliers via IQR
lines.append("===== OUTLIERS VIA IQR =====")
outlier_rows = []
for col in score_cols:
    mask, (lower, upper) = iqr_outliers(df[col])
    n_out = int(mask.sum())
    lines.append(f"{col}: outliers = {n_out}, bounds = ({lower:.2f}, {upper:.2f})")
    if n_out > 0:
        tmp = df.loc[mask, [col]].copy()
        tmp.insert(0, "column", col)
        tmp.insert(1, "index", tmp.index)
        outlier_rows.append(tmp.rename(columns={col: "value"}))
lines.append("")

# Save outlier indices
if outlier_rows:
    outliers_df = pd.concat(outlier_rows, ignore_index=True)
    outliers_df.to_csv(OUTLIERS_CSV, index=False)
else:
    pd.DataFrame(columns=["column", "index", "value"]).to_csv(OUTLIERS_CSV, index=False)

# Categorical value counts (robust column naming)
lines.append("===== CATEGORICAL VALUE COUNTS =====")
cat_counts_frames = []
for c in categorical_cols:
    vc = df[c].value_counts(dropna=False)
    lines.append(f"\n-- {c} --")
    lines.append(vc.to_string())

    # Build a tidy frame for CSV
    t = vc.rename("count").to_frame()
    t = t.assign(column=c)
    t = t.reset_index()  # creates a column typically named 'index' or the Series name
    # normalize to have 'value' column
    if "index" in t.columns and "value" not in t.columns:
        t = t.rename(columns={"index": "value"})
    # final tidy cols
    # find the value column if it's still not named 'value' for some reason
    if "value" not in t.columns:
        candidate = next((col for col in t.columns if col not in ("count", "column")), None)
        if candidate:
            t = t.rename(columns={candidate: "value"})
        else:
            t["value"] = np.nan
    t = t[["column", "value", "count"]]
    cat_counts_frames.append(t)

if cat_counts_frames:
    cat_counts = pd.concat(cat_counts_frames, ignore_index=True)
    cat_counts.to_csv(CAT_COUNTS_CSV, index=False)

# ---------- write summary ----------
with open(SUMMARY_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote sanity summary to: {SUMMARY_TXT}")
print(f"✅ Wrote outlier indices to: {OUTLIERS_CSV}")
print(f"✅ Wrote categorical value counts to: {CAT_COUNTS_CSV}")

log_run("sanity_checks.py")        