"""Celery application factory."""
from celery import Celery

from app.config import settings

celery_app = Celery(
    "geo_agent",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.workers.scan_tasks",
        "app.workers.rescan_tasks",
        "app.workers.eval_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 min max
)
