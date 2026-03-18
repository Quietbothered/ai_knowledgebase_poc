# App Root Context

## Purpose
Own package-level wiring and application entry point.

## Responsibilities
- Expose package root for imports.
- Build FastAPI app instance and mount API routers.
- Keep app bootstrap lightweight and deterministic.

## File Context Registry
| File | Purpose | Depends On | Status |
| --- | --- | --- | --- |
| `CONTEXT.md` | Root context and change tracking | `docs/AGENTS.md` | Active |
| `__init__.py` | App package marker | Python runtime | Active |
| `main.py` | FastAPI app factory and router mounting | `app/api/query_api.py`, `app/core/config.py` | Active |
| `logs/.gitkeep` | Keeps runtime log directory tracked in repository | Git | Active |
| `../.env` | Root environment variable file consumed by decouple config | `app/core/config.py` | Active |
| `../.gitignore` | Root ignore policy for runtime/build artifacts | Git | Active |

## Auth Note
Authentication is intentionally deferred. Implement auth only after explicit user instruction in chat.

## Change Log
| Date | Change | Files | Notes |
| --- | --- | --- | --- |
| 2026-03-18 | Added repository tracking and environment files at root | `../.env`, `../.gitignore` | Added default env configuration and git hygiene for tracked development |
| 2026-03-18 | Added runtime log directory tracking | `logs/.gitkeep` | Established `app/logs` as the log output directory |
| 2026-03-18 | Added initial app root scaffold tracker | `CONTEXT.md`, `__init__.py`, `main.py` | Established package bootstrap and app factory wiring |
