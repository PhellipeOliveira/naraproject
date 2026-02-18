"""Agrega todos os routers v1."""
from fastapi import APIRouter

from app.api.v1 import admin, analytics, diagnostic, feedback, privacy, waitlist

api_router = APIRouter()

api_router.include_router(
    diagnostic.router,
    prefix="/diagnostic",
    tags=["Diagnostic"],
)
api_router.include_router(
    feedback.router,
    prefix="/feedback",
    tags=["Feedback"],
)
api_router.include_router(
    waitlist.router,
    prefix="/waitlist",
    tags=["Waitlist"],
)
api_router.include_router(
    privacy.router,
    prefix="/privacy",
    tags=["Privacy"],
)
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"],
)
api_router.include_router(
    admin.router,
)
