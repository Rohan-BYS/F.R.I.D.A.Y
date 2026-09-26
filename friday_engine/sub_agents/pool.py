"""
F.R.I.D.A.Y. Sub-Agent Pool Manager.
Manages concurrency, worker allocation, task dispatching, and monitoring.
"""

from __future__ import annotations

import asyncio
from typing import Any, Callable, Dict, List, Optional
from friday_engine.config import SubAgentsConfig
from friday_engine.logger import logger
from friday_engine.sub_agents.models import SubAgentTask, TaskResult, TaskStatus
from friday_engine.sub_agents.worker import SubAgentWorker


class SubAgentPool:
    """
    Pool managing concurrent sub-agent workers.
    """

    def __init__(self, config: Optional[SubAgentsConfig] = None):
        self.config = config or SubAgentsConfig()
        self.max_workers = self.config.max_concurrent_workers
        self.workers: List[SubAgentWorker] = [
            SubAgentWorker(worker_id=f"worker-{i+1}") for i in range(self.max_workers)
        ]
        self.task_history: Dict[str, TaskResult] = {}
        self._semaphore = asyncio.Semaphore(self.max_workers)

    def get_idle_worker(self) -> Optional[SubAgentWorker]:
        """Find the first non-busy worker."""
        for worker in self.workers:
            if not worker.is_busy:
                return worker
        return None

    async def dispatch(
        self,
        goal: str,
        payload: Optional[Dict[str, Any]] = None,
        executor_func: Optional[Callable[[SubAgentTask], Any]] = None,
        timeout: Optional[int] = None,
    ) -> TaskResult:
        """Dispatch a single task to an available worker."""
        task = SubAgentTask(
            goal=goal,
            payload=payload or {},
            timeout_seconds=timeout or self.config.default_worker_timeout,
        )

        async with self._semaphore:
            worker = self.get_idle_worker() or self.workers[0]
            result = await worker.run_task(task, executor_func=executor_func)
            self.task_history[task.task_id] = result
            return result

    async def dispatch_batch(
        self,
        goals: List[str],
        executor_func: Optional[Callable[[SubAgentTask], Any]] = None,
    ) -> List[TaskResult]:
        """Dispatch multiple tasks concurrently."""
        tasks = [self.dispatch(goal=g, executor_func=executor_func) for g in goals]
        return await asyncio.gather(*tasks)

    def get_status(self) -> Dict[str, Any]:
        """Return operational status of the worker pool."""
        busy_count = sum(1 for w in self.workers if w.is_busy)
        return {
            "total_workers": len(self.workers),
            "busy_workers": busy_count,
            "idle_workers": len(self.workers) - busy_count,
            "completed_tasks": len(self.task_history),
        }
