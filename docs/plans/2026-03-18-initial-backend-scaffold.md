# Initial Backend Scaffold Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the first runnable backend scaffold for the Internal Knowledge Assistant with strict layering, typed contracts, command pattern, and per-folder context tracking.

**Architecture:** Implement `app/` in the mandated order (`api -> services -> commands -> rag -> ingestion -> models -> core`) while preserving backend-authoritative orchestration and deterministic RAG constraints. Use thin API and services, command-driven business logic, strict Pydantic models, and centralized core config/logger.

**Tech Stack:** Python 3.13, FastAPI, Pydantic v2, pytest

---

### Task 1: Project Bootstrap

**Files:**
- Create: `pyproject.toml`
- Create: `tests/__init__.py`

1. Add minimal package metadata and dependencies (`fastapi`, `pydantic`, `pytest`).
2. Add pytest config and source path settings.
3. Verify Python imports resolve from `app`.

### Task 2: RED - Query Pipeline Contract Tests

**Files:**
- Create: `tests/test_query_pipeline.py`

1. Write failing tests asserting:
- API endpoint returns standardized response shape.
- Service returns uncertainty when no retrieval evidence exists.
- Command outputs use typed models.
2. Run targeted tests and confirm failure due to missing modules/implementations.

### Task 3: GREEN - Minimal Layered Implementation

**Files:**
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `app/api/__init__.py`
- Create: `app/api/query_api.py`
- Create: `app/services/__init__.py`
- Create: `app/services/query_service.py`
- Create: `app/commands/__init__.py`
- Create: `app/commands/base_command.py`
- Create: `app/commands/generate_answer_command.py`
- Create: `app/rag/__init__.py`
- Create: `app/rag/retriever.py`
- Create: `app/ingestion/__init__.py`
- Create: `app/ingestion/connectors.py`
- Create: `app/models/__init__.py`
- Create: `app/models/enums.py`
- Create: `app/models/query_models.py`
- Create: `app/models/response_models.py`
- Create: `app/core/__init__.py`
- Create: `app/core/config.py`
- Create: `app/core/logger.py`

1. Implement strict models and enums.
2. Implement command pattern for answer construction.
3. Implement deterministic retrieval placeholder.
4. Implement service orchestration and API route.
5. Wire `FastAPI` app in `app/main.py`.

### Task 4: Context Tracking Updates

**Files:**
- Modify: `app/api/CONTEXT.md`
- Modify: `app/services/CONTEXT.md`
- Modify: `app/commands/CONTEXT.md`
- Modify: `app/rag/CONTEXT.md`
- Modify: `app/ingestion/CONTEXT.md`
- Modify: `app/models/CONTEXT.md`
- Modify: `app/core/CONTEXT.md`

1. Add new file inventory rows.
2. Append dated log entries for scaffold changes.

### Task 5: Verification

**Files:**
- No code changes expected

1. Run tests for the query pipeline.
2. Run `python -m compileall app` for syntax verification.
3. Summarize validation status and residual gaps.

## Explicit Deferral
Authentication remains deferred and must not be implemented until explicitly requested by the user.
