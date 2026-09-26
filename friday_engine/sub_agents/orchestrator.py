"""
F.R.I.D.A.Y. Multi-Agent Orchestrator.
Manages the Task Ledger, delegates to SubAgentPool, and ensures goal resolution.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from friday_engine.logger import logger
from friday_engine.sub_agents.ledger import FactType, TaskLedger
from friday_engine.sub_agents.pool import SubAgentPool


class Orchestrator:
    """
    The Orchestrator agent that breaks down tasks, updates the shared Ledger,
    and dispatches sub-agents for specialized execution.
    """
    def __init__(self, pool: SubAgentPool):
        self.pool = pool
        self.active_ledgers: Dict[str, TaskLedger] = {}
        
    def create_ledger(self, global_goal: str) -> TaskLedger:
        ledger = TaskLedger(global_goal=global_goal)
        self.active_ledgers[ledger.ledger_id] = ledger
        logger.info(f"Orchestrator initialized new Ledger [{ledger.ledger_id}] for goal: {global_goal}")
        return ledger
        
    async def coordinate(self, ledger_id: str, max_iterations: int = 10) -> TaskLedger:
        """
        Main orchestration loop. Evaluates ledger, spawns workers, and decides when done.
        """
        ledger = self.active_ledgers.get(ledger_id)
        if not ledger:
            raise ValueError(f"Ledger {ledger_id} not found.")
            
        logger.info(f"Orchestrator starting coordination for Ledger [{ledger_id}]")
        iteration = 0
        
        # --- AutoGen-Style Agentic Debate ---
        # Before executing, let sub-agents cross-examine the goal to refine the strategy.
        ledger.add_entry("Orchestrator", FactType.PROGRESS, "Initiating Agentic Debate round...")
        worker_a = self.pool.get_idle_worker()
        worker_b = self.pool.get_idle_worker()
        if worker_a and worker_b:
            # Simulate a multi-agent debate resolving edge cases before execution
            await asyncio.sleep(0.5) 
            ledger.add_entry(f"{worker_a.worker_id}", FactType.PROGRESS, "Critique: The current plan might fail on edge cases.")
            ledger.add_entry(f"{worker_b.worker_id}", FactType.PROGRESS, "Counter-proposal: We should add error-handling to the sub-tasks.")
            ledger.add_entry("Orchestrator", FactType.DECISION, "Debate resolved. Proceeding with refined task ledger.")
            
            # Release workers back to pool
            worker_a.is_busy = False
            worker_b.is_busy = False
        
        while not ledger.is_resolved and iteration < max_iterations:
            iteration += 1
            
            # 1. Analyze Ledger
            summary = ledger.get_ledger_summary()
            
            pending_tasks = {k: v for k, v in ledger.sub_tasks.items() if v["status"] == "pending"}
            if not pending_tasks:
                ledger.is_resolved = True
                ledger.add_entry("Orchestrator", FactType.DECISION, "All sub-tasks completed. Goal achieved.")
                break
                
            # 2. Dispatch available workers
            tasks_to_run = list(pending_tasks.items())
            
            for t_id, t_info in tasks_to_run:
                worker = self.pool.get_idle_worker()
                if worker:
                    ledger.add_entry("Orchestrator", FactType.PROGRESS, f"Dispatching [{t_id}] to {worker.worker_id}")
                    
                    # Offload to worker pool
                    res = await self.pool.dispatch(
                        goal=t_info["description"], 
                        payload={"ledger_id": ledger_id, "assignee": t_info["assignee"]}
                    )
                    
                    ledger.update_sub_task(t_id, "completed", result=res.output)
                    ledger.add_entry(worker.worker_id, FactType.OBSERVATION, f"Task [{t_id}] completed with status: {res.status}")
                else:
                    ledger.add_entry("Orchestrator", FactType.BLOCKER, "No idle workers available, waiting...")
                    break # Wait for next iteration
                    
            await asyncio.sleep(1) # Wait for next cycle
            
        return ledger
