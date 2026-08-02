"""Service: Closed-loop Re-measurement engine.

Khi task.status = done:
1. Re-scan các prompt E-commerce liên quan (3 lần × 4 AI)
2. Tính pre/post difference với **bootstrap 95% CI**
3. Phân loại: improved / no_evidence / regressed

Theo arXiv 2603.08924:
- Noise floor = 5-7 điểm %
- Improved phải vượt noise floor
- Dùng bootstrap CI, KHÔNG dùng point estimate
"""
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task
from app.config import settings


def bootstrap_diff_ci(
    pre_samples: list[float], post_samples: list[float], n_iter: int = 1000, alpha: float = 0.05
) -> tuple[float, float]:
    """Bootstrap 95% CI cho difference (post - pre).

    Args:
        pre_samples: visibility rates pre-action (vd: 3 lần/prompt, nhiều prompt)
        post_samples: visibility rates post-action
        n_iter: số lần bootstrap (default 1000)
        alpha: significance level (default 0.05 cho 95% CI)

    Returns:
        (ci_lower, ci_upper)
    """
    if not pre_samples or not post_samples:
        return (0.0, 0.0)
    rng = np.random.default_rng(seed=42)
    diffs = []
    for _ in range(n_iter):
        pre_boot = rng.choice(pre_samples, size=len(pre_samples), replace=True)
        post_boot = rng.choice(post_samples, size=len(post_samples), replace=True)
        diffs.append(post_boot.mean() - pre_boot.mean())
    diffs = np.array(diffs)
    ci_lower = float(np.percentile(diffs, 100 * alpha / 2))
    ci_upper = float(np.percentile(diffs, 100 * (1 - alpha / 2)))
    return (ci_lower, ci_upper)


def classify_closed_loop(
    pre_visibility: float, post_visibility: float, ci_lower: float, ci_upper: float
) -> str:
    """Phân loại: improved / no_evidence / regressed.

    Logic:
        - Nếu ci_lower > noise_floor → improved (vượt noise floor 5-7%)
        - Nếu ci_upper < -noise_floor → regressed
        - Ngược lại → no_evidence
    """
    noise_floor = settings.noise_floor_pct / 100.0  # convert 0.06 → 0.06
    if ci_lower > noise_floor:
        return "improved"
    if ci_upper < -noise_floor:
        return "regressed"
    return "no_evidence"


async def evaluate_task(session: AsyncSession, task_id: int) -> dict:
    """Đánh giá closed-loop cho 1 task.

    Returns:
        Dict với pre/post visibility, CI, result.
    """
    task = await session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}

    # TODO: thực tế cần scan lại 3 lần × 4 AI để có post_samples
    # Tạm thời trả về placeholder
    pre_visibility = task.pre_visibility or 0.0
    post_visibility = task.post_visibility or 0.0
    diff = post_visibility - pre_visibility

    # Mock CI (chưa có re-scan thật)
    # TODO: thay bằng bootstrap_diff_ci khi có data thật
    ci_lower = diff - 0.05
    ci_upper = diff + 0.05

    result = classify_closed_loop(pre_visibility, post_visibility, ci_lower, ci_upper)
    task.ci_lower = ci_lower
    task.ci_upper = ci_upper
    task.result = result
    await session.commit()

    return {
        "task_id": task_id,
        "pre_visibility": pre_visibility,
        "post_visibility": post_visibility,
        "diff": diff,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "noise_floor": settings.noise_floor_pct / 100.0,
        "result": result,
    }
