import pandas as pd
import sys
import os
from pathlib import Path
from datetime import datetime
import numpy as np

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
DATA_FILE = SCRIPT_DIR.parent / "data" / "StudentsPerformance.csv"
OUT_DIR = SCRIPT_DIR.parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "descriptive_stats.txt"

# ---------- dual output ----------
class DualOutput:
    def __init__(self, *files):
        self.files = files
    def write(self, msg):
        for f in self.files:
            f.write(msg)
    def flush(self):
        for f in self.files:
            try:
                f.flush()
            except Exception:
                pass

_real_stdout = sys.__stdout__

with open(OUT_FILE, "w", encoding="utf-8") as output_file:
    sys.stdout = DualOutput(_real_stdout, output_file)
    try:
        # -------- your analysis --------
        df = pd.read_csv(DATA_FILE)
        df["total_score"] = df["math score"] + df["reading score"] + df["writing score"]
        df["average_score"] = df["total_score"] / 3

        print("===== Basic Dataset Info =====")
        print("Number of records:", len(df))
        print("Columns:", list(df.columns))
        print("\nUnique values per column:\n", df.nunique())

        print("\n===== Descriptive Stats for Individual Scores =====")
        score_cols = ["math score", "reading score", "writing score"]
        print(df[score_cols].describe())

        print("\n===== Correlation Between Scores =====")
        print(df[score_cols].corr())

        print("\n===== Top 5 Students by Total Score =====")
        print(df.sort_values("total_score", ascending=False).head(5)[["gender", "race/ethnicity", "total_score"]])

        print("\n===== Bottom 5 Students by Total Score =====")
        print(df.sort_values("total_score").head(5)[["gender", "race/ethnicity", "total_score"]])

        print("\n===== Best and Worst Subject for Each Student (Sample 5) =====")
        df["best_subject"] = df[score_cols].idxmax(axis=1)
        df["worst_subject"] = df[score_cols].idxmin(axis=1)
        print(df[["math score", "reading score", "writing score", "best_subject", "worst_subject"]].head(5))

        print("\n===== Score Categories =====")
        def categorize(score):
            if score < 150:
                return "Failing"
            elif score < 210:
                return "Average"
            else:
                return "Excellent"
        df["performance_category"] = df["total_score"].apply(categorize)
        print(df["performance_category"].value_counts())

        print("\n===== Average Total Score by Gender =====")
        print(df.groupby("gender")["total_score"].mean())

        print("\n===== Average Total Score by Parental Education =====")
        print(df.groupby("parental level of education")["total_score"].mean().sort_values(ascending=False))

        print("\n===== Average Total Score by Test Prep Course =====")
        print(df.groupby("test preparation course")["total_score"].mean())

        print("\n===== Underperforming Students (total_score < 150) =====")
        print(df[df["total_score"] < 150][["gender", "parental level of education", "test preparation course", "total_score"]].head())
        # -----------------------------------------
    finally:
        sys.stdout = _real_stdout

log_run("descriptive_stats.py")       
