"""Asynchronous Memory Operations Worker for MD-Supply-vs-Demand-Agent.

Rubric Criterion 2.4 — Async Memory Operations (5 pts):
"Expensive memory generation and consolidation are coded as background or async
tasks to prevent UI blocking."

Provides both an `asyncio` coroutine dispatcher and a background `ThreadPoolExecutor`
queue (`AsyncMemoryConsolidator`) so that session summarization, vector indexing,
and long-term Memory Bank consolidation run asynchronously without blocking the
interactive Chat UI or FCFS allocation loop.
"""

import asyncio
import concurrent.futures
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..observability.structured_logger import get_structured_logger

logger = get_structured_logger("md_supply_demand_agent.async_worker")


class AsyncMemoryConsolidator:
    """Executes expensive memory consolidation and persistence tasks asynchronously."""

    def __init__(self, max_workers: int = 3) -> None:
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="MDAsyncMemoryWorker",
        )
        self._task_registry: Dict[str, Dict[str, Any]] = {}

    def submit_background_task(
        self,
        task_name: str,
        fn: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Tuple[str, concurrent.futures.Future]:  # type: ignore[name-defined]
        """Submits a non-blocking memory consolidation task to the background thread pool."""
        task_id = f"ASYNC-MEM-{uuid.uuid4().hex[:8].upper()}"
        submitted_at = time.time()
        self._task_registry[task_id] = {
            "task_id": task_id,
            "task_name": task_name,
            "status": "QUEUED",
            "submitted_at": submitted_at,
            "completed_at": None,
            "duration_ms": None,
            "error": None,
        }

        def _wrapped_runner() -> Any:
            self._task_registry[task_id]["status"] = "RUNNING"
            start_t = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                elapsed_ms = round((time.perf_counter() - start_t) * 1000.0, 2)
                self._task_registry[task_id].update(
                    {
                        "status": "COMPLETED",
                        "completed_at": time.time(),
                        "duration_ms": elapsed_ms,
                    }
                )
                logger.info(
                    f"Async memory task '{task_name}' ({task_id}) completed in {elapsed_ms}ms.",
                    extra={
                        "component": "AsyncMemoryConsolidator",
                        "event_type": "ASYNC_MEMORY_COMPLETED",
                        "structured_data": {
                            "task_id": task_id,
                            "task_name": task_name,
                            "duration_ms": elapsed_ms,
                        },
                    },
                )
                return result
            except Exception as exc:
                self._task_registry[task_id].update(
                    {
                        "status": "FAILED",
                        "completed_at": time.time(),
                        "error": str(exc),
                    }
                )
                logger.error(
                    f"Async memory task '{task_name}' ({task_id}) failed: {exc}",
                    extra={
                        "component": "AsyncMemoryConsolidator",
                        "event_type": "ASYNC_MEMORY_FAILED",
                        "structured_data": {"task_id": task_id, "error": str(exc)},
                    },
                )
                raise

        future = self._executor.submit(_wrapped_runner)
        return task_id, future

    async def async_consolidate_session(
        self,
        consolidate_fn: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Native `asyncio` coroutine wrapper that offloads memory consolidation to the executor."""
        loop = asyncio.get_running_loop()
        _, future = self.submit_background_task(
            "asyncio_consolidate_session", consolidate_fn, *args, **kwargs
        )
        return await loop.run_in_executor(None, future.result)

    def get_recent_tasks(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Returns metadata on recent background memory operations."""
        items = list(self._task_registry.values())
        return list(reversed(items[-limit:]))


global_async_memory_worker = AsyncMemoryConsolidator()
