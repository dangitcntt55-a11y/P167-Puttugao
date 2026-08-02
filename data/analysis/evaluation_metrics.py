"""Evaluation metrics — precision/recall/F1 cho mention parser."""
import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


def load_gold(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute precision/recall/F1."""
    if df.empty:
        return {"precision": 0, "recall": 0, "f1": 0, "n_samples": 0}

    y_true = df["is_correct"].astype(int)
    y_pred = df["is_target_brand"].astype(int)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred).tolist()

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "n_samples": len(df),
        "n_target": int(y_true.sum()),
        "n_found": int(y_pred.sum()),
        "confusion_matrix": cm,
    }


def compute_metrics_by_group(df: pd.DataFrame, group_col: str) -> dict:
    """Compute metrics per group (e.g., per prompt group hoặc AI engine)."""
    return {
        group: compute_metrics(group_df)
        for group, group_df in df.groupby(group_col)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True, help="Gold dataset CSV")
    parser.add_argument("--predictions", required=True, help="Predictions CSV từ parser")
    parser.add_argument("--group-by", default="ai_engine", help="ai_engine | prompt_group")
    parser.add_argument("--output", default="evaluation_report.json")
    args = parser.parse_args()

    gold = load_gold(args.gold)
    predictions = pd.read_csv(args.predictions)

    # Merge
    merged = gold.merge(predictions, on="response_id", suffixes=("_gold", "_pred"))

    overall = compute_metrics(merged)
    by_group = compute_metrics_by_group(merged, args.group_by)

    report = {
        "overall": overall,
        "by_group": by_group,
        "target_f1": overall["f1"],
        "passed": overall["f1"] >= 0.85,
    }

    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"✅ Evaluation report → {out_path}")
    print(f"  - Precision: {overall['precision']}")
    print(f"  - Recall: {overall['recall']}")
    print(f"  - F1: {overall['f1']} (target ≥ 0.85)")


if __name__ == "__main__":
    main()
