import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# -------- paths --------
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA_FILE = ROOT / "data" / "StudentsPerformance.csv"
FIG_DIR = ROOT / "report" / "figures"
LOG_DIR = ROOT / "outputs" / "logs"
FIG_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42  # for reproducibility (if any random sampling later)
np.random.seed(SEED)

def log(msg: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / "run.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] visuals.py | {msg}\n")

def savefig(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

# -------- load & derive --------
df = pd.read_csv(DATA_FILE)
score_cols = ["math score", "reading score", "writing score"]
df["total_score"] = df["math score"] + df["reading score"] + df["writing score"]
df["average_score"] = df["total_score"] / 3

def categorize(total):
    if total < 150:
        return "Failing"
    elif total < 210:
        return "Average"
    else:
        return "Excellent"
df["performance_category"] = df["total_score"].apply(categorize)

# -------- FIGURE 1: Histograms of scores --------
for col in score_cols:
    plt.figure()
    plt.hist(df[col].dropna().values, bins=20)
    plt.title(f"Distribution of {col.title()}")
    plt.xlabel(col.title())
    plt.ylabel("Count")
    savefig(FIG_DIR / f"hist_{col.replace(' ', '_')}.png")
log("Saved histograms for math/reading/writing")

# -------- FIGURE 2: Boxplot of total_score by gender --------
plt.figure()
groups = [g for g in df["gender"].dropna().unique()]
data = [df.loc[df["gender"] == g, "total_score"].dropna().values for g in groups]
plt.boxplot(data, labels=[str(g) for g in groups], showfliers=True)
plt.title("Total Score by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Score")
savefig(FIG_DIR / "box_total_by_gender.png")
log("Saved boxplot of total_score by gender")

# -------- FIGURE 3: Bar chart of performance category distribution --------
cat_counts = df["performance_category"].value_counts().reindex(["Excellent","Average","Failing"], fill_value=0)
plt.figure()
plt.bar(cat_counts.index.astype(str), cat_counts.values)
plt.title("Performance Category Distribution")
plt.xlabel("Category")
plt.ylabel("Number of Students")
savefig(FIG_DIR / "bar_performance_category.png")
log("Saved bar chart of performance categories")

print(f"✅ Figures written to: {FIG_DIR}")
print(f"📝 Log written to: {LOG_DIR / 'run.log'}")
