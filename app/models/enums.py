"""Centralized enumerations for the application."""

from __future__ import annotations

from enum import Enum


class SourceType(str, Enum):
    """Supported ingestion and retrieval sources."""

    TEAMS = "teams"
    SHAREPOINT = "sharepoint"
    JIRA = "jira"


class ConnectorMode(str, Enum):
    """Supported ingestion synchronization modes."""

    FULL = "full"
    INCREMENTAL = "incremental"
