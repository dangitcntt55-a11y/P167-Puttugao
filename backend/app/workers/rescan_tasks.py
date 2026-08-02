"""Celery tasks for closed-loop re-scan."""
from app.workers.celery_app import celery_app


@celery_app.task(name="rescan.trigger_after_task_done")
def trigger_rescan(task_id: int) -> dict:
    """Trigger re-scan sau khi task.status = done.

    Args:
        task_id: ID của task vừa được đánh dấu done

    Returns:
        Dict: {task_id, status, post_scan_id}
    """
    # TODO: thực tế cần:
    # 1. Lấy task → lấy diagnosis → lấy prompt_ids
    # 2. Re-scan 3 lần × 4 AI
    # 3. Lưu post_scan_id vào task
    # 4. Trigger eval task
    return {
        "task_id": task_id,
        "status": "re_scan_triggered",
        "post_scan_id": None,
        "message": "TODO: integrate with agent/ + eval",
    }
