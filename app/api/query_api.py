"""HTTP API for query requests."""

from __future__ import annotations

from fastapi import APIRouter

from app.services.query_service import QueryService

router: APIRouter = APIRouter()
_query_service: QueryService = QueryService()


@router.get("/query")
def query_endpoint(query: str) -> object:
    """Handle query requests using service orchestration."""

    try:
        return _query_service.answer_user_query(query=query)
    except Exception as exc:
        raise Exception(f"[query_endpoint] {str(exc)}") from exc
