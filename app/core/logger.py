"""Central structured logger implementation."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import SETTINGS


class AthenaLogger:
    """Structured JSON logger that enforces the ATHENA logging contract."""

    def __init__(
        self,
        service: str,
        level: str = "INFO",
        log_dir: str | Path = "app/logs",
        log_file_name: str = "app.log",
    ) -> None:
        self._logger: logging.Logger = logging.getLogger(service)
        self._logger.setLevel(level.upper())
        self._logger.propagate = False

        if not self._logger.handlers:
            log_dir_path = Path(log_dir)
            log_dir_path.mkdir(parents=True, exist_ok=True)

            formatter = logging.Formatter("%(message)s")

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

            file_handler = logging.FileHandler(log_dir_path / log_file_name, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        self._service: str = service

    def info(
        self,
        module: str,
        class_name: str,
        method: str,
        message: str,
        request_id: str = "",
        status_code: int = 0,
        latency_ms: int = 0,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level="INFO",
            module=module,
            class_name=class_name,
            method=method,
            message=message,
            request_id=request_id,
            status_code=status_code,
            latency_ms=latency_ms,
            extra=extra,
        )

    def warning(
        self,
        module: str,
        class_name: str,
        method: str,
        message: str,
        request_id: str = "",
        status_code: int = 0,
        latency_ms: int = 0,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level="WARNING",
            module=module,
            class_name=class_name,
            method=method,
            message=message,
            request_id=request_id,
            status_code=status_code,
            latency_ms=latency_ms,
            extra=extra,
        )

    def error(
        self,
        module: str,
        class_name: str,
        method: str,
        message: str,
        request_id: str = "",
        status_code: int = 0,
        latency_ms: int = 0,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level="ERROR",
            module=module,
            class_name=class_name,
            method=method,
            message=message,
            request_id=request_id,
            status_code=status_code,
            latency_ms=latency_ms,
            extra=extra,
        )

    def debug(
        self,
        module: str,
        class_name: str,
        method: str,
        message: str,
        request_id: str = "",
        status_code: int = 0,
        latency_ms: int = 0,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level="DEBUG",
            module=module,
            class_name=class_name,
            method=method,
            message=message,
            request_id=request_id,
            status_code=status_code,
            latency_ms=latency_ms,
            extra=extra,
        )

    def _emit(
        self,
        level: str,
        module: str,
        class_name: str,
        method: str,
        message: str,
        request_id: str,
        status_code: int,
        latency_ms: int,
        extra: dict[str, Any] | None,
    ) -> None:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": self._service,
            "module": module,
            "class": class_name,
            "method": method,
            "message": message,
            "request_id": request_id,
            "status_code": status_code,
            "latency_ms": latency_ms,
            "extra": extra or {},
        }
        log_line: str = json.dumps(payload, ensure_ascii=True)

        if level == "ERROR":
            self._logger.error(log_line)
        elif level == "WARNING":
            self._logger.warning(log_line)
        elif level == "DEBUG":
            self._logger.debug(log_line)
        else:
            self._logger.info(log_line)


ATHENA_LOGGER: AthenaLogger = AthenaLogger(
    service=SETTINGS.service_name,
    level=SETTINGS.log_level,
    log_dir=SETTINGS.log_dir,
    log_file_name=SETTINGS.log_file_name,
)
