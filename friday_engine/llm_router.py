"""
Top-level re-export for LLM Router to satisfy friday_engine/llm_router.py interface.
"""

from friday_engine.llm.base import (
    BaseLLMProvider,
    LLMAuthenticationError,
    LLMError,
    LLMMessage,
    LLMRateLimitError,
    LLMResponse,
    LLMTimeoutError,
    Role,
)
from friday_engine.llm.router import LLMRouter

__all__ = [
    "LLMRouter",
    "BaseLLMProvider",
    "LLMMessage",
    "LLMResponse",
    "Role",
    "LLMError",
    "LLMAuthenticationError",
    "LLMRateLimitError",
    "LLMTimeoutError",
]
