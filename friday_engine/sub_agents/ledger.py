"""
F.R.I.D.A.Y. Multi-Agent Ledger System (Magentic-One Architecture).
Implements a shared Task Ledger/Blackboard for decentralized agent coordination.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from friday_engine.logger import logger

class FactType(str, Enum):
    OBSERVATION = "observation"
    DECISION = "decision"
    PROGRESS = "progress"
    BLOCKER = "blocker"
    CODE_ARTIFACT = "code_artifact"

@dataclass
class LedgerEntry:
    fact_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    agent_name: str = "System"
    fact_type: FactType = FactType.OBSERVATION
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class TaskLedger:
    """
    Central Blackboard / Shared Memory for multi-agent coordination.
    All sub-agents read from and write to this ledger to prevent duplicated work
    and to share discoveries.
    """
    def __init__(self, global_goal: str):
        self.ledger_id = str(uuid.uuid4())[:8]
        self.global_goal = global_goal
        self.entries: List[LedgerEntry] = []
        self.sub_tasks: Dict[str, Dict[str, Any]] = {}
        self.is_resolved: bool = False
        self.created_at = time.time()
        
    def add_entry(self, agent_name: str, fact_type: FactType, content: str, metadata: Optional[Dict[str, Any]] = None) -> LedgerEntry:
        entry = LedgerEntry(
            agent_name=agent_name,
            fact_type=fact_type,
            content=content,
            metadata=metadata or {}
        )
        self.entries.append(entry)
        logger.debug(f"[Ledger:{self.ledger_id}] {agent_name} added {fact_type.value}: {content[:50]}...")
        return entry
        
    def get_entries(self, fact_type: Optional[FactType] = None, limit: int = 50) -> List[LedgerEntry]:
        if fact_type:
            filtered = [e for e in self.entries if e.fact_type == fact_type]
            return filtered[-limit:]
        return self.entries[-limit:]
        
    def add_sub_task(self, task_id: str, description: str, assignee: str):
        self.sub_tasks[task_id] = {
            "description": description,
            "assignee": assignee,
            "status": "pending",
            "result": None
        }
        
    def update_sub_task(self, task_id: str, status: str, result: Any = None):
        if task_id in self.sub_tasks:
            self.sub_tasks[task_id]["status"] = status
            if result:
                self.sub_tasks[task_id]["result"] = result
                
    def get_ledger_summary(self) -> str:
        """Generates a text summary of the ledger state for LLM context."""
        summary = f"Global Goal: {self.global_goal}\n"
        summary += f"Status: {'Resolved' if self.is_resolved else 'In Progress'}\n\n"
        
        summary += "--- Sub-Tasks ---\n"
        if not self.sub_tasks:
            summary += "None.\n"
        for k, v in self.sub_tasks.items():
            summary += f"- [{k}] {v['description']} (Assignee: {v['assignee']}, Status: {v['status']})\n"
            
        summary += "\n--- Recent Ledger Entries ---\n"
        for entry in self.entries[-10:]:
            summary += f"[{entry.agent_name} | {entry.fact_type.value.upper()}] {entry.content}\n"
            
        return summary
