"""Application configuration definitions."""

from __future__ import annotations

import os
from pathlib import Path

from decouple import AutoConfig
from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    """Strongly typed application settings loaded from environment variables."""

    model_config = ConfigDict(extra="forbid")

    service_name: str = Field(default="knowledge-assistant-backend")
    api_prefix: str = Field(default="/api/v1")
    log_level: str = Field(default="INFO")
    log_dir: str = Field(default="app/logs")
    log_file_name: str = Field(default="app.log")

    @classmethod
    def from_env(cls, search_path: Path | str | None = None) -> "Settings":
        """Load runtime settings from environment variables and .env files."""

        config_search_path = search_path or Path(__file__).resolve().parents[2]
        decouple_config = AutoConfig(search_path=str(config_search_path))

        return cls(
            service_name=decouple_config(
                "SERVICE_NAME",
                default=os.getenv("SERVICE_NAME", "knowledge-assistant-backend"),
                cast=str,
            ),
            api_prefix=decouple_config(
                "API_PREFIX",
                default=os.getenv("API_PREFIX", "/api/v1"),
                cast=str,
            ),
            log_level=decouple_config(
                "LOG_LEVEL",
                default=os.getenv("LOG_LEVEL", "INFO"),
                cast=str,
            ),
            log_dir=decouple_config(
                "LOG_DIR",
                default=os.getenv("LOG_DIR", "app/logs"),
                cast=str,
            ),
            log_file_name=decouple_config(
                "LOG_FILE_NAME",
                default=os.getenv("LOG_FILE_NAME", "app.log"),
                cast=str,
            ),
        )


SETTINGS: Settings = Settings.from_env()
