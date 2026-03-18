# AGENTS.md — Codex Operating Rules (Zero-Ambiguity Spec)

## Overview

This repository contains the design and implementation plan for an Internal Knowledge Assistant (RAG system).

Codex acts as a **software engineer** responsible for implementing the system based strictly on the documentation in `/docs`.

Codex MUST follow all rules defined here when generating or modifying code.

---

# 0. Rule Priority Order (MANDATORY)

If any rules conflict, follow this order:

1. Explanation-First Development Rule (Section 12.1)
2. Core Architecture Rule (Section 3)
3. Type Safety, Logging, Response & Exception Rules (Section 6)
4. Project Structure & Import Rules (Section 5)
5. Code Style Rules (Section 6)

Codex MUST NOT violate higher-priority rules.

---

# 1. Repository State

The repository is currently in the **design-first phase**.

* Most logic exists in `/docs`
* Production code is not yet implemented

Codex responsibilities:

* Translate design documents into code
* Create initial project structure
* Implement features incrementally

Codex MUST NOT assume implementations exist unless present.

---

# 2. Source of Truth

System behavior MUST align with:

* `docs/01-architecture/`
* `docs/02-ingestion/`
* `docs/04-llm/`
* `docs/ai/ai-guardrails.md`

If conflicts arise:

→ Architecture docs take priority

---

# 3. Core Architecture Rule (STRICT)

## Backend-Authoritative Model

Backend (FastAPI) controls:

* orchestration
* retrieval flow
* prompt construction
* validation

LLM (via LlamaIndex) ONLY:

* retrieval
* response generation

Codex MUST NOT:

* move logic into prompts
* introduce agents
* allow LLM to make system decisions

---

# 4. Implementation Strategy (MANDATORY ORDER)

1. Project structure
2. API layer
3. Service layer
4. Command layer
5. RAG layer
6. Connectors
7. Indexing
8. Retrieval

Codex MUST NOT skip layers.

---

# 5. Project Structure Rules (STRICT)

```
app/
 ├── api/
 ├── services/
 ├── commands/
 ├── rag/
 ├── ingestion/
 ├── models/
 └── core/
```

---

## Import Rules (STRICT)

* api → services
* services → commands, rag, models
* commands → models, core
* rag → core, models
* core → no upward imports

❌ Circular imports prohibited.

---

# 6. Engineering Rules (STRICT)

---

## 6.1 Code Style Rules

* Language: Python
* Type hints REQUIRED everywhere
* Class-based design REQUIRED
* Small focused functions only

---

## 6.2 Command Pattern (MANDATORY)

All business logic MUST exist inside command classes.

* Services orchestrate commands ONLY
* Services MUST NOT contain business logic

Example:

```python
class BaseCommand:
    def execute(self):
        raise NotImplementedError
```

---

## 6.3 Standard Response Rules (MANDATORY)

All API responses MUST use:

```python
class BaseResponse(BaseModel):
    status: int
    message: str
    data: dict
```

❌ Returning dicts prohibited.

---

## 6.4 Pydantic Type Safety Rules (STRICT)

Pydantic MUST be used for:

* API inputs
* API outputs
* command inputs
* service structured inputs
* external integrations

---

### Function Rules

* All public methods MUST use type hints
* Structured inputs MUST use models
* Outputs MUST use models

---

### Constructor Rules

Constructors MUST use typed params or models.

---

### Strict Mode

```python
class Config:
    extra = "forbid"
```

---

### Prohibited

❌ dicts for structured data
❌ `.dict()` before boundary
❌ mixing raw dict + model

---

## 6.5 Enum Rules (STRICT)

All enums MUST be defined in:

```
app/models/enums.py
```

❌ Duplicate enums prohibited.

---

## 6.6 Status Code Rules

Use ONLY:

```python
from fastapi import status
```

❌ No hardcoded numbers.

---

## 6.7 Exception Rules (STRICT)

Required for:

* commands
* services
* integrations

Optional for small utils.

Format:

```python
raise Exception(f"[Class.method] {str(e)}")
```

---

## 6.8 Logging Rules (STRICT — ATHENA READY)

### Central Logger

Must exist:

```
app/core/logger.py
```

Modules MUST NOT create loggers.

---

### Log Format

```json
{
  "timestamp": "ISO8601",
  "level": "INFO|ERROR|WARNING|DEBUG",
  "service": "string",
  "module": "string",
  "class": "string",
  "method": "string",
  "message": "string",
  "request_id": "string",
  "status_code": int,
  "latency_ms": int,
  "extra": {}
}
```

---

### Prohibited

❌ print()
❌ string logs
❌ sensitive data

---

## 6.9 Configuration Rules

All configs MUST be in:

```
app/core/config.py
```

❌ Hardcoded values prohibited.

---

## 6.10 Consistency Rules

Codex MUST enforce:

* response consistency
* enum consistency
* logging consistency
* validation consistency

---

# 7. Dependency Rules

Allowed:

* FastAPI
* LlamaIndex
* Pinecone
* HuggingFace

No new libs without justification.

---

# 8. Change Safety Rules

* minimal diffs only
* no breaking changes
* no file deletion without approval

---

# 9. RAG Rules

* retrieval ALWAYS before generation
* no hardcoded answers

---

# 10. Prompt Rules

* deterministic prompts only
* no business logic in prompts

---

# 11. Error Handling

* no silent failures
* explicit exceptions only

---

# 12. Workflow Rules

---

## 12.1 Explanation-First Rule (STRICT)

Before coding, Codex MUST provide:

1. Problem Understanding
2. Proposed Approach
3. Components Involved
4. Data Flow
5. Justification

Codex MUST wait for approval.

---

## 12.2 Validation Before Completion (MANDATORY)

Codex MUST verify:

* response compliance
* enum usage
* logging compliance
* Pydantic compliance
* no hardcoded values

---

# 13. Definition of Done

Task complete ONLY if:

* architecture aligned
* rules followed
* code clean
* no violations

---

# 14. Non-Goals

Codex MUST NOT:

* redesign architecture
* change stack
* introduce agents

---

# 15. Enforcement Philosophy

If rules conflict:

→ Codex MUST stop and flag issue.

---
