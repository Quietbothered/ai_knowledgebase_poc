# Teams Mixed-Mode Connector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace deterministic Teams seed ingestion with real Microsoft Graph ingestion supporting two runtime-selectable modes (`channel_messages` and `get_all_messages`) while preserving safe seed fallback.

**Architecture:** Keep the existing connector abstraction and ingestion pipeline intact. Extend `TeamsConnector` with an internal Graph HTTP client, mode resolution from env-backed settings, and normalized `IngestionDocument` mapping. Implement mode switching via config and verify behavior through TDD with focused unit tests.

**Tech Stack:** Python 3.13, FastAPI project conventions, Pydantic settings models, stdlib `urllib` HTTP client, pytest.

---

### Task 1: Expand settings model for Teams mixed-mode configuration

**Files:**
- Modify: `app/core/config.py`
- Modify: `.env`
- Test: `tests/test_config.py`

**Step 1: Write the failing test**

Add assertions in `tests/test_config.py` that `Settings.from_env()` loads Teams connector settings from `.env` values.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -q`
Expected: FAIL because new settings fields are missing.

**Step 3: Write minimal implementation**

Add Teams settings fields in `Settings` and `from_env()` for:
- mode and graph enablement
- tenant/client credentials
- team/channel targeting
- pagination and incremental lookback
- source metadata defaults

Update root `.env` with commented/default values for these keys.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -q`
Expected: PASS.

### Task 2: Add failing tests for Teams connector mixed modes

**Files:**
- Create: `tests/test_teams_connector.py`
- Modify: `app/ingestion/connectors.py`

**Step 1: Write the failing test**

Add tests that validate:
- seed mode returns deterministic document when graph disabled
- `channel_messages` mode normalizes Graph response into `IngestionDocument`
- `get_all_messages` mode uses incremental date filter for incremental sync
- error is raised when graph mode selected without required credentials

Use a fake HTTP transport callable injection so tests never call external network.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_teams_connector.py -q`
Expected: FAIL before implementation.

**Step 3: Write minimal implementation**

Implement Teams connector mode resolution and Graph fetch methods with:
- token acquisition
- endpoint-specific URL construction
- page traversal with `@odata.nextLink`
- HTML/text normalization
- metadata mapping and strict logging

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_teams_connector.py -q`
Expected: PASS.

### Task 3: Keep ingestion pipeline compatibility and manual verification path

**Files:**
- Modify: `app/ingestion/connectors.py`
- Test: `tests/test_ingestion_indexing_pipeline.py`

**Step 1: Write the failing test**

Extend pipeline test to confirm default connector mode remains safe (`seed`) and pipeline still completes without external credentials.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_ingestion_indexing_pipeline.py -q`
Expected: FAIL if defaults/regression mismatch.

**Step 3: Write minimal implementation**

Adjust Teams connector defaults and validation logic so pipeline behavior remains deterministic locally while allowing explicit graph modes via env.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_ingestion_indexing_pipeline.py -q`
Expected: PASS.

### Task 4: Document Microsoft Teams setup and runtime mode usage

**Files:**
- Modify: `README.md`
- Modify: `app/ingestion/CONTEXT.md`
- Modify: `app/core/CONTEXT.md`
- Modify: `app/CONTEXT.md`

**Step 1: Write docs updates**

Add Teams section in README covering:
- app registration in Microsoft Entra
- application permissions and admin consent
- required env vars per mode
- API endpoint behavior differences and caveats
- manual ingestion test steps

Update folder context files with exact files changed and rationale.

**Step 2: Verify docs consistency**

Run: `rg -n "Teams|AUTO_INGESTION|LOG_DIR|connector mode|graph" README.md app/*/CONTEXT.md app/CONTEXT.md`
Expected: references present and coherent.

### Task 5: End-to-end verification

**Files:**
- Test: `tests/test_config.py`
- Test: `tests/test_teams_connector.py`
- Test: `tests/test_ingestion_indexing_pipeline.py`
- Test: `tests/test_ingestion_to_retrieval_integration.py`

**Step 1: Run targeted tests**

Run:
- `pytest tests/test_config.py tests/test_teams_connector.py tests/test_ingestion_indexing_pipeline.py tests/test_ingestion_to_retrieval_integration.py -q`
Expected: all pass.

**Step 2: Run full suite**

Run: `pytest -q`
Expected: full suite passes with no newly introduced regressions.
