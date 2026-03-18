"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator, Callable

from fastapi import FastAPI

from app.api.query_api import router as query_router
from app.core.config import SETTINGS
from app.core.logger import ATHENA_LOGGER
from app.ingestion.automation import AutoIngestionRuntime
from app.models.enums import ConnectorMode


def _resolve_auto_ingestion_mode(mode_value: str) -> ConnectorMode:
    """Resolve configured auto-ingestion mode with safe fallback."""

    try:
        resolved_mode = ConnectorMode(mode_value.lower())
        ATHENA_LOGGER.info(
            module="app.main",
            class_name="ApplicationFactory",
            method="_resolve_auto_ingestion_mode",
            message="Resolved auto-ingestion mode from configuration",
            extra={"configured_mode": mode_value, "resolved_mode": resolved_mode.value},
        )
        return resolved_mode
    except Exception:
        ATHENA_LOGGER.warning(
            module="app.main",
            class_name="ApplicationFactory",
            method="_resolve_auto_ingestion_mode",
            message="Invalid auto-ingestion mode configured; using incremental fallback",
            extra={"configured_mode": mode_value, "fallback_mode": ConnectorMode.INCREMENTAL.value},
        )
        return ConnectorMode.INCREMENTAL


def _build_lifespan(
    auto_ingestion_runtime: AutoIngestionRuntime,
    auto_ingestion_enabled: bool,
) -> Callable[[FastAPI], AsyncContextManager[None]]:
    """Build FastAPI lifespan handler for application runtime lifecycle."""

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            ATHENA_LOGGER.info(
                module="app.main",
                class_name="ApplicationFactory",
                method="lifespan.startup",
                message="Application lifespan startup received",
                extra={"auto_ingestion_enabled": auto_ingestion_enabled},
            )
            auto_ingestion_runtime.start()
            ATHENA_LOGGER.info(
                module="app.main",
                class_name="ApplicationFactory",
                method="lifespan.startup",
                message="Application lifespan startup completed",
                extra={"auto_ingestion_running": auto_ingestion_runtime.is_running},
            )
        except Exception as exc:
            ATHENA_LOGGER.error(
                module="app.main",
                class_name="ApplicationFactory",
                method="lifespan.startup",
                message="Application lifespan startup failed",
                extra={"error": str(exc), "auto_ingestion_enabled": auto_ingestion_enabled},
            )
            raise Exception(f"[lifespan.startup] {str(exc)}") from exc

        try:
            yield
        finally:
            ATHENA_LOGGER.info(
                module="app.main",
                class_name="ApplicationFactory",
                method="lifespan.shutdown",
                message="Application lifespan shutdown received",
                extra={"auto_ingestion_enabled": auto_ingestion_enabled},
            )
            try:
                auto_ingestion_runtime.stop()
                ATHENA_LOGGER.info(
                    module="app.main",
                    class_name="ApplicationFactory",
                    method="lifespan.shutdown",
                    message="Application lifespan shutdown completed",
                    extra={"auto_ingestion_running": auto_ingestion_runtime.is_running},
                )
            except Exception as exc:
                ATHENA_LOGGER.error(
                    module="app.main",
                    class_name="ApplicationFactory",
                    method="lifespan.shutdown",
                    message="Application lifespan shutdown failed",
                    extra={"error": str(exc), "auto_ingestion_enabled": auto_ingestion_enabled},
                )
                raise Exception(f"[lifespan.shutdown] {str(exc)}") from exc

    return lifespan


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    auto_ingestion_runtime = AutoIngestionRuntime(
        enabled=SETTINGS.auto_ingestion_enabled,
        mode=_resolve_auto_ingestion_mode(SETTINGS.auto_ingestion_mode),
        interval_seconds=SETTINGS.auto_ingestion_interval_seconds,
    )

    app = FastAPI(
        title="Internal Knowledge Assistant API",
        lifespan=_build_lifespan(
            auto_ingestion_runtime=auto_ingestion_runtime,
            auto_ingestion_enabled=SETTINGS.auto_ingestion_enabled,
        ),
    )
    app.include_router(query_router, prefix=SETTINGS.api_prefix)

    return app


app: FastAPI = create_app()
