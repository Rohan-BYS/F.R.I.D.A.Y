"""
Local LLM Provider.
Integrates with local inference engines (llama.cpp server, Ollama, LM Studio, or local API).
"""

from __future__ import annotations

from typing import List, Optional
from friday_engine.llm.base import LLMMessage, LLMResponse
from friday_engine.llm.openai_provider import OpenAIProvider


class LocalLLMProvider(OpenAIProvider):
    """
    Local LLM Provider inherits from OpenAI-compatible provider,
    pointing to local server endpoints (default http://127.0.0.1:8000/v1 or http://localhost:11434/v1).
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000/v1",
        model: str = "llama-3-8b-instruct",
        timeout: int = 60,
        temperature: float = 0.2,
    ):
        super().__init__(
            api_key="local-not-required",
            model=model,
            base_url=base_url,
            timeout=timeout,
            temperature=temperature,
        )
        self.name = "local"
