# Folder Context Tracking Design

## Problem Understanding
We need per-folder markdown files in `app/` that preserve architecture context and track changes to files as development proceeds.

## Proposed Approach
Create `CONTEXT.md` in each required application folder:
- `app/api/`
- `app/services/`
- `app/commands/`
- `app/rag/`
- `app/ingestion/`
- `app/models/`
- `app/core/`

Each file contains:
- purpose and responsibilities
- architecture boundaries/import constraints
- file context registry
- dated change log
- auth deferral note

## Components Involved
- `docs/AGENTS.md`
- architecture docs under `docs/01-architecture`, `docs/02-ingestion`, `docs/04-llm`, `docs/03-operations`, and `docs/ai`
- new `app/*/CONTEXT.md` files

## Data Flow
1. A file is added or modified under a folder.
2. The matching folder `CONTEXT.md` is updated in the same change set.
3. `File Context Registry` tracks file purpose/dependencies.
4. `Change Log` appends date + summary + touched files.

## Justification
- Keeps documentation local to each module.
- Improves onboarding and design traceability.
- Enforces architecture boundaries from `docs/AGENTS.md`.
- Supports incremental, auditable development.

## Explicit Deferral
Authentication implementation is deferred and will only start when explicitly requested by the user in chat.
