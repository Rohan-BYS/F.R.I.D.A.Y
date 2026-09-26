"""
F.R.I.D.A.Y. Engine State and Session Memory.
Tracks runtime health, execution history, active sub-agent tasks, and goals.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from friday_engine.llm.base import LLMMessage, Role


class EngineStatus(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    THINKING = "thinking"
    EXECUTING = "executing"
    HEALING = "self_healing"
    SHUTTING_DOWN = "shutting_down"


@dataclass
class SessionMemory:
    """Manages conversational messages and episodic context."""
    messages: List[LLMMessage] = field(default_factory=list)
    max_history_turns: int = 50

    def add_message(self, role: Role | str, content: str) -> None:
        self.messages.append(LLMMessage(role=role, content=content))
        # Keep message history bounded
        if len(self.messages) > self.max_history_turns * 2:
            # Preserve system instruction if first message
            if self.messages and self.messages[0].role == Role.SYSTEM:
                sys_msg = self.messages[0]
                self.messages = [sys_msg] + self.messages[-((self.max_history_turns * 2) - 1):]
            else:
                self.messages = self.messages[-(self.max_history_turns * 2):]

    def clear(self) -> None:
        self.messages.clear()


@dataclass
class FridayState:
    status: EngineStatus = EngineStatus.INITIALIZING
    start_time: float = field(default_factory=time.time)
    goals_completed: int = 0
    tools_forged: int = 0
    active_tasks: Dict[str, Any] = field(default_factory=dict)
    memory: SessionMemory = field(default_factory=SessionMemory)
    last_error: Optional[str] = None

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time
