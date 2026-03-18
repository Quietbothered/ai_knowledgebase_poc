"""Tests for environment-backed settings loading."""

from __future__ import annotations

from pathlib import Path

from app.core.config import Settings


def test_settings_from_env_reads_values_from_dotenv_file(tmp_path: Path) -> None:
    """Settings loader should read values from a .env file search path."""

    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "SERVICE_NAME=kb-test-service",
                "API_PREFIX=/api/test/v1",
                "LOG_LEVEL=DEBUG",
                "LOG_DIR=app/logs",
                "LOG_FILE_NAME=test.log",
                "AUTO_INGESTION_ENABLED=true",
                "AUTO_INGESTION_INTERVAL_SECONDS=900",
                "AUTO_INGESTION_MODE=incremental",
            ]
        ),
        encoding="utf-8",
    )

    settings = Settings.from_env(search_path=tmp_path)

    assert settings.service_name == "kb-test-service"
    assert settings.api_prefix == "/api/test/v1"
    assert settings.log_level == "DEBUG"
    assert settings.log_dir == "app/logs"
    assert settings.log_file_name == "test.log"
    assert settings.auto_ingestion_enabled is True
    assert settings.auto_ingestion_interval_seconds == 900
    assert settings.auto_ingestion_mode == "incremental"
