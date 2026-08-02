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
    """Đánh giá closed-loop cho 1 task — thật, không mock.

    Flow:
        1. Lấy task → có brand_id, prompt_ids (lưu trong action_payload).
        2. Query pre_visibility: từ bảng stability_scores hoặc responses tại thời điểm pre.
        3. Query post_visibility: từ responses mới nhất (sau khi re-scan đã chạy).
        4. Tính bootstrap 95% CI cho diff.
        5. Phân loại improved/no_evidence/regressed.
        6. Update task.result, task.ci_lower, task.ci_upper.
    """
    from sqlalchemy import select, and_
    from app.db.models import Response, StabilityScore

    task = await session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}

    # Lấy related prompt_ids từ task.action_payload
    prompt_ids: list[int] = (task.action_payload or {}).get("prompt_ids", [])
    if not prompt_ids:
        return {"error": "Task has no prompt_ids in action_payload"}

    # Pre/post samples: visibility per (brand, prompt, llm_engine) từ N lần chạy
    pre_window_start = task.created_at  # gần thời điểm tạo task

    async def collect_visibility(window_start, window_end):
        """Lấy list visibility_rate per (prompt, llm_engine) trong khoảng thời gian."""
        q = (
            select(StabilityScore)
            .where(
                StabilityScore.brand_id == task.brand_id,
                StabilityScore.prompt_id.in_(prompt_ids),
                StabilityScore.computed_at >= window_start,
                StabilityScore.computed_at < window_end,
            )
        )
        result = await session.execute(q)
        scores = result.scalars().all()
        return [float(s.visibility_rate) for s in scores]

    pre_samples = await collect_visibility(window_start=pre_window_start, window_end=task.completed_at or task.created_at)
    post_samples = await collect_visibility(window_start=task.completed_at or task.created_at, window_end="now")

    if not pre_samples or not post_samples:
        return {"error": "Missing pre or post data — ensure re-scan has run"}

    ci = bootstrap_diff_ci(pre_samples, post_samples)
    result = classify_closed_loop(pre_visibility=sum(pre_samples) / len(pre_samples), post_visibility=sum(post_samples) / len(post_samples), ci_lower=ci[0], ci_upper=ci[1])

    task.pre_visibility = sum(pre_samples) / len(pre_samples)
    task.post_visibility = sum(post_samples) / len(post_samples)
    task.ci_lower = ci[0]
    task.ci_upper = ci[1]
    task.result = result
    await session.commit()

    return {"task_id": task_id, "pre_visibility": task.pre_visibility, "post_visibility": task.post_visibility, "ci_lower": ci[0], "ci_upper": ci[1], "result": result}
