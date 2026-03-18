"""Connector scaffolds for supported ingestion sources."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.logger import ATHENA_LOGGER
from app.models.enums import ConnectorMode, SourceType


class BaseConnector(ABC):
    """Base connector interface for ingestion sources."""

    source_type: SourceType

    @abstractmethod
    def fetch_documents(self, mode: ConnectorMode) -> list[str]:
        """Fetch source documents for ingestion."""

        raise NotImplementedError


class TeamsConnector(BaseConnector):
    """Microsoft Teams connector placeholder."""

    source_type = SourceType.TEAMS

    def fetch_documents(self, mode: ConnectorMode) -> list[str]:
        try:
            ATHENA_LOGGER.info(
                module="app.ingestion.connectors",
                class_name="TeamsConnector",
                method="fetch_documents",
                message="Teams connector placeholder invoked",
                extra={"mode": mode.value},
            )
            return []
        except Exception as exc:
            raise Exception(f"[TeamsConnector.fetch_documents] {str(exc)}") from exc


class SharePointConnector(BaseConnector):
    """Microsoft SharePoint connector placeholder."""

    source_type = SourceType.SHAREPOINT

    def fetch_documents(self, mode: ConnectorMode) -> list[str]:
        try:
            ATHENA_LOGGER.info(
                module="app.ingestion.connectors",
                class_name="SharePointConnector",
                method="fetch_documents",
                message="SharePoint connector placeholder invoked",
                extra={"mode": mode.value},
            )
            return []
        except Exception as exc:
            raise Exception(f"[SharePointConnector.fetch_documents] {str(exc)}") from exc


class JiraConnector(BaseConnector):
    """Jira connector placeholder."""

    source_type = SourceType.JIRA

    def fetch_documents(self, mode: ConnectorMode) -> list[str]:
        try:
            ATHENA_LOGGER.info(
                module="app.ingestion.connectors",
                class_name="JiraConnector",
                method="fetch_documents",
                message="Jira connector placeholder invoked",
                extra={"mode": mode.value},
            )
            return []
        except Exception as exc:
            raise Exception(f"[JiraConnector.fetch_documents] {str(exc)}") from exc
