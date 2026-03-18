# Ingestion Folder Context

## Purpose
Own data connector, preprocessing, chunking, and indexing workflows for knowledge ingestion.

## Responsibilities
- Integrate source connectors (Teams, SharePoint, Jira).
- Handle full backfill and incremental updates.
- Normalize content and preserve meaningful structure.
- Produce chunked, metadata-rich artifacts for embedding/indexing.

## Boundaries
- Primary references: `docs/02-ingestion/connectors_and_indexing.md`.
- Keep ingestion deterministic and auditable.
- Avoid introducing auth implementation here until explicitly requested.

## File Context Registry
| File | Purpose | Depends On | Status |
| --- | --- | --- | --- |
| `CONTEXT.md` | Folder context and change tracking | `docs/AGENTS.md`, ingestion docs | Active |
| `__init__.py` | Ingestion package marker | Python runtime | Active |
| `connectors.py` | Connector base class and source connector placeholders | `app/models/enums.py`, `app/core/logger.py` | Active |

## Auth Note
Authentication is intentionally deferred. Implement auth only after explicit user instruction in chat.

## Change Log
| Date | Change | Files | Notes |
| --- | --- | --- | --- |
| 2026-03-18 | Added explicit integration exception wrapping | `connectors.py` | Applied required exception format for connector integration boundaries |
| 2026-03-18 | Added initial ingestion scaffold files | `__init__.py`, `connectors.py` | Added connector interfaces/placeholders for Teams, SharePoint, and Jira |
| 2026-03-18 | Initialized ingestion folder context tracker | `CONTEXT.md` | Prepared connector/indexing tracking |
