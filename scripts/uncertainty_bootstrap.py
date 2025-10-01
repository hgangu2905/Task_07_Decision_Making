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
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "StudentsPerformance.csv"
OUT_FILE = Path(__file__).resolve().parent.parent / "outputs" / "uncertainty_cis.csv"

# ---------- load data ----------
df = pd.read_csv(DATA_FILE)

# Add derived columns (same as in descriptive_stats.py)
df["total_score"] = df["math score"] + df["reading score"] + df["writing score"]
df["average_score"] = df["total_score"] / 3

# ---------- bootstrap confidence intervals ----------
n_boot = 1000
cols_to_check = ["math score", "reading score", "writing score", "total_score", "average_score"]

results = {}
for col in cols_to_check:
    data = df[col].dropna().values
    means = [np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_boot)]
    ci_low, ci_high = np.percentile(means, [2.5, 97.5])
    results[col] = {"mean": np.mean(data), "ci_low": ci_low, "ci_high": ci_high}

# ---------- save results ----------
pd.DataFrame(results).T.to_csv(OUT_FILE)
print("✅ Saved bootstrap CI results to:", OUT_FILE)

log_run("uncertainity_bootstrap.py")      
