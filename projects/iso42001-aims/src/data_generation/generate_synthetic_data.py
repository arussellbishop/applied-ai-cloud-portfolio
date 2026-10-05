"""Generate deterministic, fictional student-intervention data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed"
SEED = 42001

def make(n: int, drift: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(SEED + (1 if drift else 0))
    age = rng.choice(["16-17", "18-20", "21-24", "25+"], n, p=[.25,.35,.25,.15])
    gender = rng.choice(["group_a", "group_b", "not_stated"], n, p=[.47,.47,.06])
    attendance = np.clip(rng.normal(84 if not drift else 74, 10, n), 35, 100)
    performance = np.clip(rng.normal(68 if not drift else 63, 15, n), 0, 100)
    engagement = np.clip(rng.normal(3.5 if not drift else 3.0, .8, n), 1, 5)
    interventions = rng.poisson(0.7 if not drift else 1.2, n)
    support = rng.binomial(1, .18 if not drift else .25, n)
    logit = (-0.4 + (70-attendance)*.045 + (55-performance)*.025 + (3-engagement)*.5
             + interventions*.28 + support*.55)
    probability = 1/(1+np.exp(-logit))
    outcome = rng.binomial(1, probability)
    return pd.DataFrame({
        "student_id": [f"SYN-{i:05d}" for i in range(n)], "age_band": age,
        "course": rng.choice(["STEM", "Arts", "Business", "Health"], n),
        "attendance": attendance.round(2), "assessment_performance": performance.round(2),
        "engagement": engagement.round(2), "prior_interventions": interventions,
        "support_need": support, "gender_group": gender, "outcome": outcome,
    })

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make(4000).to_csv(OUT / "student_intervention_baseline.csv", index=False)
    make(4000, True).to_csv(OUT / "student_intervention_drift.csv", index=False)
    print(f"Generated deterministic synthetic datasets in {OUT}")

if __name__ == "__main__":
    main()
