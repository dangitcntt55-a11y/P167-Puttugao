"""Stability analysis — phân tích Stability Score từ responses.

Compute:
- Stability Score per (brand, prompt)
- % gap đạt Stability >= 0.7
- Mean/median stability
- Stability distribution
"""
import argparse
from pathlib import Path
import json
import csv

import numpy as np
import pandas as pd


def compute_stability_score(mention_counts: list[int]) -> float:
    """1 - normalized variance."""
    if not mention_counts:
        return 0.0
    arr = np.array(mention_counts, dtype=float)
    var = arr.var()
    max_var = 0.25
    return float(1.0 - min(var / max_var, 1.0))


def load_responses(csv_path: str) -> pd.DataFrame:
    """Load responses từ CSV (export từ backend)."""
    expected_cols = [
        "response_id", "brand_id", "prompt_id", "ai_engine",
        "run_index", "is_target_brand"
    ]
    return pd.read_csv(csv_path)


def analyze_stability(df: pd.DataFrame, threshold: float = 0.7) -> dict:
    """Analyze stability across all (brand, prompt) pairs."""
    # Group by (brand_id, prompt_id, ai_engine) → list of mention counts
    grouped = df.groupby(["brand_id", "prompt_id", "ai_engine"])["is_target_brand"].apply(list).reset_index()
    grouped["stability_score"] = grouped["is_target_brand"].apply(compute_stability_score)
    grouped["is_stable"] = grouped["stability_score"] >= threshold

    n_total = len(grouped)
    n_stable = grouped["is_stable"].sum()
    pct_stable = n_stable / n_total if n_total else 0

    return {
        "n_total_gaps": n_total,
        "n_stable_gaps": int(n_stable),
        "pct_stable": round(pct_stable, 3),
        "mean_stability": round(grouped["stability_score"].mean(), 3),
        "median_stability": round(grouped["stability_score"].median(), 3),
        "threshold": threshold,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV responses từ backend")
    parser.add_argument("--output", default="stability_report.json")
    parser.add_argument("--threshold", type=float, default=0.7)
    args = parser.parse_args()

    df = load_responses(args.input)
    report = analyze_stability(df, args.threshold)

    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"✅ Stability report → {out_path}")
    print(f"  - Total gaps: {report['n_total_gaps']}")
    print(f"  - Stable (≥ {threshold}): {report['n_stable_gaps']} ({report['pct_stable']*100:.1f}%)")
    print(f"  - Mean stability: {report['mean_stability']}")


if __name__ == "__main__":
    main()
