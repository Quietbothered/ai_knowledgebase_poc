"""Tests for Teams connector mixed-mode ingestion behavior."""

from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import unquote_plus

import pytest

from app.core.config import Settings
from app.ingestion.connectors import TeamsConnector
from app.models.enums import ConnectorMode, SourceType


class _FakeGraphTransport:
    def __init__(self, get_responses: list[dict] | None = None) -> None:
        self._get_responses = get_responses or []
        self.get_urls: list[str] = []
        self.post_urls: list[str] = []
        self.post_payloads: list[dict[str, str]] = []
        self._get_index = 0

    def post_form(
        self,
        url: str,
        data: dict[str, str],
        timeout_seconds: int,
    ) -> dict:
        self.post_urls.append(url)
        self.post_payloads.append(data)
        return {"access_token": "test-token"}

    def get_json(
        self,
        url: str,
        headers: dict[str, str],
        timeout_seconds: int,
    ) -> dict:
        self.get_urls.append(url)
        if self._get_index >= len(self._get_responses):
            return {"value": []}
        payload = self._get_responses[self._get_index]
        self._get_index += 1
        return payload


def _build_settings(**overrides: object) -> Settings:
    return Settings().model_copy(update=overrides)


def test_teams_connector_seed_mode_returns_deterministic_document() -> None:
    """Seed mode should continue returning deterministic sample payload."""

    connector = TeamsConnector(
        settings=_build_settings(
            teams_connector_mode="seed",
            teams_graph_enabled=False,
            teams_source_name="Teams Platform Channel",
        )
    )

    result = connector.fetch_documents(mode=ConnectorMode.FULL)

    assert len(result.documents) == 1
    assert result.documents[0].metadata.source_type == SourceType.TEAMS
    assert result.documents[0].metadata.source_name == "Teams Platform Channel"


def test_teams_connector_channel_messages_mode_normalizes_graph_messages() -> None:
    """Channel messages mode should fetch Graph data and normalize into ingestion docs."""

    transport = _FakeGraphTransport(
        get_responses=[
            {
                "value": [
                    {
                        "id": "msg-100",
                        "createdDateTime": "2026-03-18T10:00:00Z",
                        "lastModifiedDateTime": "2026-03-18T10:01:00Z",
                        "subject": "Release update",
                        "from": {"user": {"displayName": "Alice"}},
                        "body": {"contentType": "html", "content": "<p>Hello <b>team</b></p>"},
                    }
                ]
            }
        ]
    )
    connector = TeamsConnector(
        settings=_build_settings(
            teams_connector_mode="channel_messages",
            teams_graph_enabled=True,
            teams_tenant_id="tenant-1",
            teams_client_id="client-1",
            teams_client_secret="secret-1",
            teams_team_id="team-1",
            teams_channel_id="channel-1",
            teams_source_name="Teams Platform Channel",
            teams_project_key="KB",
            teams_confidentiality="internal",
            teams_page_size=10,
            teams_max_pages=2,
        ),
        transport=transport,
    )

    result = connector.fetch_documents(mode=ConnectorMode.FULL)

    assert len(result.documents) == 1
    assert result.documents[0].metadata.document_id == "msg-100"
    assert result.documents[0].metadata.author == "Alice"
    assert result.documents[0].metadata.source_name == "Teams Platform Channel"
    assert result.documents[0].metadata.title == "Release update"
    assert result.documents[0].text == "Hello team"
    assert len(transport.post_urls) == 1
    assert len(transport.get_urls) == 1


def test_teams_connector_get_all_messages_incremental_adds_graph_filter() -> None:
    """Get-all-messages mode should add incremental lastModifiedDateTime filter."""

    transport = _FakeGraphTransport(get_responses=[{"value": []}])
    connector = TeamsConnector(
        settings=_build_settings(
            teams_connector_mode="get_all_messages",
            teams_graph_enabled=True,
            teams_tenant_id="tenant-1",
            teams_client_id="client-1",
            teams_client_secret="secret-1",
            teams_team_id="team-1",
            teams_source_name="Teams Platform Channel",
            teams_incremental_lookback_seconds=3600,
        ),
        transport=transport,
        now_provider=lambda: datetime(2026, 3, 18, 12, 0, 0, tzinfo=timezone.utc),
    )

    connector.fetch_documents(mode=ConnectorMode.INCREMENTAL)

    assert len(transport.get_urls) == 1
    decoded_url = unquote_plus(transport.get_urls[0])
    assert "channels/getAllMessages" in decoded_url
    assert "lastModifiedDateTime gt 2026-03-18T11:00:00Z" in decoded_url


def test_teams_connector_graph_mode_requires_credentials() -> None:
    """Graph-enabled mode should fail fast when required credentials are missing."""

    connector = TeamsConnector(
        settings=_build_settings(
            teams_connector_mode="channel_messages",
            teams_graph_enabled=True,
            teams_tenant_id="",
            teams_client_id="",
            teams_client_secret="",
            teams_team_id="team-1",
            teams_channel_id="channel-1",
        )
    )

    with pytest.raises(Exception, match=r"\[TeamsConnector.fetch_documents\]"):
        connector.fetch_documents(mode=ConnectorMode.FULL)
