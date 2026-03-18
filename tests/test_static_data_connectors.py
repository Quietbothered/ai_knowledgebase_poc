"""Tests for local static chat/document ingestion connectors."""

from __future__ import annotations

from pathlib import Path

from app.core.config import Settings
from app.ingestion.connectors import LocalChatDataConnector, LocalDocumentsConnector
from app.models.enums import ConnectorMode, SourceType


def test_local_chat_connector_loads_all_chat_json_messages() -> None:
    """Local chat connector should ingest messages from all chat_data JSON files."""

    connector = LocalChatDataConnector(
        settings=Settings().model_copy(
            update={
                "static_chat_data_dir": "app/data/chat_data",
                "static_project_key": "KB",
                "static_confidentiality": "internal",
            }
        )
    )

    result = connector.fetch_documents(mode=ConnectorMode.FULL)
    expected_file_count = len(list(Path("app/data/chat_data").glob("*.json")))

    assert expected_file_count > 0
    assert len(result.documents) >= expected_file_count
    assert all(doc.metadata.source_type == SourceType.TEAMS for doc in result.documents)
    assert all("Local Chat Data /" in doc.metadata.source_name for doc in result.documents)


def test_local_documents_connector_loads_all_docx_documents() -> None:
    """Local documents connector should ingest text from every .docx in documents folder."""

    connector = LocalDocumentsConnector(
        settings=Settings().model_copy(
            update={
                "static_documents_dir": "app/data/documents",
                "static_project_key": "KB",
                "static_confidentiality": "internal",
            }
        )
    )

    result = connector.fetch_documents(mode=ConnectorMode.FULL)
    expected_doc_count = len(list(Path("app/data/documents").glob("*.docx")))

    assert expected_doc_count > 0
    assert len(result.documents) == expected_doc_count
    assert all(doc.metadata.source_type == SourceType.SHAREPOINT for doc in result.documents)
    assert all(len(doc.text) > 100 for doc in result.documents)
