"""Query, retrieval, and answer payload models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SourceType


class RetrievalChunk(BaseModel):
    """Retrieved chunk candidate used for answer construction."""

    model_config = ConfigDict(extra="forbid")

    source_type: SourceType
    source_name: str
    excerpt: str


class RetrievalRequest(BaseModel):
    """Service input for document retrieval."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)


class RetrievalResult(BaseModel):
    """Output produced by retrieval stage before generation."""

    model_config = ConfigDict(extra="forbid")

    chunks: list[RetrievalChunk]
