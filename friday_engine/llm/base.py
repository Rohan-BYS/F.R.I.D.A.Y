"""
Base interfaces and data structures for LLM Providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class LLMMessage:
    role: Role | str
    content: str
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": str(self.role.value if isinstance(self.role, Role) else self.role),
            "content": self.content,
        }


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    raw_response: Optional[Dict[str, Any]] = None
    input_tokens: int = 0
    output_tokens: int = 0
    latency_seconds: float = 0.0
    finish_reason: Optional[str] = None


class LLMError(Exception):
    """Base exception for all LLM errors."""
    pass


class LLMAuthenticationError(LLMError):
    """Raised when authentication/API key is invalid or missing."""
    pass


class LLMRateLimitError(LLMError):
    """Raised when rate limits are exceeded."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when request times out."""
    pass


class BaseLLMProvider(ABC):
    """Abstract interface that every LLM provider must implement."""

    def __init__(self, name: str, model: str, timeout: int = 30):
        self.name = name
        self.model = model
        self.timeout = timeout
        self.is_healthy: bool = True
        self.failure_count: int = 0

    @abstractmethod
    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        """Execute a chat completion request."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if provider endpoint and credentials are operational."""
        pass

    def record_success(self) -> None:
        self.is_healthy = True
        self.failure_count = 0

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= 3:
            self.is_healthy = False
