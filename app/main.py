"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.query_api import router as query_router
from app.core.config import SETTINGS


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(title="Internal Knowledge Assistant API")
    app.include_router(query_router, prefix=SETTINGS.api_prefix)
    return app


app: FastAPI = create_app()
