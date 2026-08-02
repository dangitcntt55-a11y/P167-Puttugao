"""API v1 package."""
from fastapi import APIRouter

from app.api.v1 import brands, prompts, scan, visibility, diagnoses, tasks, evaluation

api_router = APIRouter()
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(scan.router, prefix="/scan", tags=["scan"])
api_router.include_router(visibility.router, prefix="/visibility", tags=["visibility"])
api_router.include_router(diagnoses.router, prefix="/diagnoses", tags=["diagnoses"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
