"""
Data models for F.R.I.D.A.Y. Persistent Memory & State Engine.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class MessageRecord:
    session_id: str
    role: MessageRole | str
    content: str
    id: Optional[int] = None
    tool_name: Optional[str] = None
    tool_calls: Optional[str] = None
    metadata_json: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": str(self.role.value if isinstance(self.role, MessageRole) else self.role),
            "content": self.content,
            "tool_name": self.tool_name,
            "tool_calls": self.tool_calls,
            "created_at": self.created_at,
        }


@dataclass
class SessionRecord:
    session_id: str
    title: str = "Active Session"
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    is_archived: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemorySearchResult:
    message_id: int
    session_id: str
    role: str
    content: str
    snippet: str
    rank: float
    created_at: float


class SkillMetadata(BaseModel):
    name: str
    description: str
    category: str = "general"
    version: str = "1.0.0"
    author: str = "F.R.I.D.A.Y. Evolution"
    created_at: float = Field(default_factory=time.time)
    tags: List[str] = Field(default_factory=list)
