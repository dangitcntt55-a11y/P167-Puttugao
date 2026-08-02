"""Celery tasks for evaluation (bootstrap CI + closed-loop classification)."""
from app.workers.celery_app import celery_app


@celery_app.task(name="eval.compute_closed_loop")
def compute_closed_loop(task_id: int) -> dict:
    """Compute closed-loop evaluation: bootstrap CI + classify.

    Args:
        task_id: ID của task

    Returns:
        Dict: {task_id, result, ci_lower, ci_upper, ...}
    """
    # TODO: integrate with services/closed_loop.py
    return {
        "task_id": task_id,
        "status": "evaluated",
        "message": "TODO: integrate with closed_loop service",
    }
