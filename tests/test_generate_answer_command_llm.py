"""Tests for LLM-backed answer generation behavior."""

from __future__ import annotations

import json

from app.commands.generate_answer_command import GenerateAnswerCommand, GenerateAnswerInput
from app.models.enums import SourceType
from app.models.query_models import RetrievalChunk


class _StubHuggingFaceClient:
    def __init__(self, response_text: str, should_fail: bool = False) -> None:
        self._response_text = response_text
        self._should_fail = should_fail
        self.calls = 0

    def generate_answer(self, query: str, context_chunks: list[RetrievalChunk]) -> str:
        self.calls += 1
        if self._should_fail:
            raise RuntimeError("simulated hf failure")
        return self._response_text


def _sample_chunks() -> list[RetrievalChunk]:
    return [
        RetrievalChunk(
            source_type=SourceType.TEAMS,
            source_name="Local Chat Data / team_chat_1.json",
            excerpt="The team discussed scaling pain and cloud cost growth.",
        ),
        RetrievalChunk(
            source_type=SourceType.SHAREPOINT,
            source_name="Local Documents / proposal.docx",
            excerpt="The proposal suggests staged microservices migration.",
        ),
    ]


def test_generate_answer_command_uses_hf_response_when_available() -> None:
    """Command should use parsed HF JSON response when API call succeeds."""

    client = _StubHuggingFaceClient(
        response_text=json.dumps(
            {
                "summary": "DeepSeek summary",
                "detailed_explanation": "DeepSeek detailed answer from static sources.",
            }
        )
    )
    command = GenerateAnswerCommand(hf_client=client)

    output = command.execute(
        GenerateAnswerInput(
            query="What is the modernization recommendation?",
            retrieved_chunks=_sample_chunks(),
        )
    )

    assert output.summary == "DeepSeek summary"
    assert output.detailed_explanation == "DeepSeek detailed answer from static sources."
    assert len(output.sources) == 2
    assert client.calls == 1


def test_generate_answer_command_falls_back_when_hf_call_fails() -> None:
    """Command should gracefully fallback to deterministic formatting on HF errors."""

    client = _StubHuggingFaceClient(response_text="", should_fail=True)
    command = GenerateAnswerCommand(hf_client=client)

    output = command.execute(
        GenerateAnswerInput(query="Summarize rollout risk", retrieved_chunks=_sample_chunks())
    )

    assert output.summary == "Answer generated from retrieved internal sources"
    assert "The team discussed scaling pain" in output.detailed_explanation
    assert len(output.sources) == 2
    assert client.calls == 1
