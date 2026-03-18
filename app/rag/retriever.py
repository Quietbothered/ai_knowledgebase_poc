"""Retrieval layer entry point."""

from __future__ import annotations

from app.core.logger import ATHENA_LOGGER
from app.models.query_models import RetrievalRequest, RetrievalResult


class Retriever:
    """Deterministic retrieval facade.

    Current scaffold intentionally returns no chunks until connectors and indexing are wired.
    """

    def retrieve(self, request: RetrievalRequest) -> RetrievalResult:
        """Retrieve relevant chunks for a user query."""

        try:
            ATHENA_LOGGER.info(
                module="app.rag.retriever",
                class_name="Retriever",
                method="retrieve",
                message="Retrieval executed with placeholder backend",
                extra={"query": request.query},
            )
            return RetrievalResult(chunks=[])
        except Exception as exc:  # pragma: no cover - defensive boundary
            raise Exception(f"[Retriever.retrieve] {str(exc)}") from exc
