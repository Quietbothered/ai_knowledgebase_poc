"""Tests for centralized logging behavior."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.core.logger import AthenaLogger


def test_athena_logger_writes_json_log_file_to_configured_directory(tmp_path: Path) -> None:
    """AthenaLogger must write logs to a file in the configured log directory."""

    logger = AthenaLogger(
        service=f"test-service-{uuid4().hex}",
        level="INFO",
        log_dir=tmp_path,
        log_file_name="test.log",
    )

    logger.info(
        module="tests.test_logger",
        class_name="LoggerTests",
        method="test_athena_logger_writes_json_log_file_to_configured_directory",
        message="log file contract test",
    )

    log_file = tmp_path / "test.log"
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "log file contract test" in content
    assert '"level": "INFO"' in content
