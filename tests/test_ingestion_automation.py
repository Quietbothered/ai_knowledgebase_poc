"""Tests for automatic ingestion scheduling runtime."""

from __future__ import annotations

from threading import Event

from app.ingestion.automation import AutoIngestionRuntime, IngestionScheduler
from app.models.enums import ConnectorMode


class _StubPipeline:
    def __init__(self, event: Event | None = None) -> None:
        self.run_calls: list[ConnectorMode] = []
        self._event = event

    def run(self, mode: ConnectorMode, chunk_size_tokens: int = 600, chunk_overlap_tokens: int = 80):
        self.run_calls.append(mode)
        if self._event is not None:
            self._event.set()
        return {
            "status": "completed",
            "documents_processed": 1,
            "chunks_created": 1,
            "chunks_indexed": 1,
            "index_name": "stub_index",
        }


def test_ingestion_scheduler_run_once_executes_pipeline() -> None:
    """Scheduler run_once should execute pipeline immediately with configured mode."""

    pipeline = _StubPipeline()
    scheduler = IngestionScheduler(
        pipeline=pipeline,
        mode=ConnectorMode.FULL,
        interval_seconds=60,
    )

    scheduler.run_once()

    assert pipeline.run_calls == [ConnectorMode.FULL]


def test_ingestion_scheduler_start_triggers_background_run() -> None:
    """Scheduler start should trigger an immediate background run and allow clean stop."""

    run_event = Event()
    pipeline = _StubPipeline(event=run_event)
    scheduler = IngestionScheduler(
        pipeline=pipeline,
        mode=ConnectorMode.INCREMENTAL,
        interval_seconds=60,
    )

    scheduler.start()
    assert run_event.wait(timeout=1.0)
    scheduler.stop()

    assert len(pipeline.run_calls) >= 1
    assert pipeline.run_calls[0] == ConnectorMode.INCREMENTAL


def test_auto_ingestion_runtime_respects_enabled_flag() -> None:
    """Runtime should not start scheduler when auto ingestion is disabled."""

    pipeline = _StubPipeline()
    runtime = AutoIngestionRuntime(
        enabled=False,
        mode=ConnectorMode.FULL,
        interval_seconds=60,
        pipeline=pipeline,
    )

    runtime.start()
    runtime.stop()

    assert pipeline.run_calls == []
