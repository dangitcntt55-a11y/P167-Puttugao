"""Bootstrap CI — compute 95% CI for closed-loop evaluation.

Theo arXiv 2603.08924:
- 1000 iterations
- alpha = 0.05 (95% CI)
- Compare post vs pre visibility
"""
import argparse
import json
from pathlib import Path

import numpy as np


def bootstrap_diff_ci(
    pre_samples: list[float],
    post_samples: list[float],
    n_iter: int = 1000,
    alpha: float = 0.05,
    seed: int = 42,
) -> dict:
    """Bootstrap 95% CI for difference (post - pre).

    Args:
        pre_samples: pre-action visibility rates
        post_samples: post-action visibility rates
        n_iter: số lần bootstrap
        alpha: significance level

    Returns:
        Dict with mean_diff, ci_lower, ci_upper, p_value
    """
    rng = np.random.default_rng(seed=seed)
    if not pre_samples or not post_samples:
        return {"mean_diff": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "p_value": 1.0}

    diffs = []
    for _ in range(n_iter):
        pre_boot = rng.choice(pre_samples, size=len(pre_samples), replace=True)
        post_boot = rng.choice(post_samples, size=len(post_samples), replace=True)
        diffs.append(post_boot.mean() - pre_boot.mean())

    diffs = np.array(diffs)
    ci_lower = float(np.percentile(diffs, 100 * alpha / 2))
    ci_upper = float(np.percentile(diffs, 100 * (1 - alpha / 2)))

    # p-value: proportion of diffs that cross 0
    p_value = float((np.abs(diffs) > 0).mean() if (diffs > 0).all() else (diffs <= 0).mean())

    return {
        "mean_diff": float(diffs.mean()),
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": p_value,
        "n_iter": n_iter,
    }


def classify(noise_floor: float = 0.06, **kwargs) -> str:
    """Classify: improved / no_evidence / regressed."""
    ci_lower = kwargs.get("ci_lower", 0.0)
    ci_upper = kwargs.get("ci_upper", 0.0)

    if ci_lower > noise_floor:
        return "improved"
    if ci_upper < -noise_floor:
        return "regressed"
    return "no_evidence"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pre", required=True, help="JSON list pre-visibility")
    parser.add_argument("--post", required=True, help="JSON list post-visibility")
    parser.add_argument("--output", default="bootstrap_ci.json")
    parser.add_argument("--n-iter", type=int, default=1000)
    args = parser.parse_args()

    pre = json.loads(Path(args.pre).read_text())
    post = json.loads(Path(args.post).read_text())

    result = bootstrap_diff_ci(pre, post, n_iter=args.n_iter)
    result["classification"] = classify(**result)
    result["noise_floor"] = 0.06

    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Bootstrap CI → {out_path}")
    print(f"  - Mean diff: {result['mean_diff']:.4f}")
    print(f"  - 95% CI: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]")
    print(f"  - Classification: {result['classification']}")


if __name__ == "__main__":
    main()
