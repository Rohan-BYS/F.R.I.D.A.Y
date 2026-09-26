"""
F.R.I.D.A.Y. Multi-LLM Router.
Orchestrates requests across multiple LLM backends (Gemini, Claude, OpenAI, Local)
with automatic fallback, priority ordering, health-tracking, and telemetry.
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Union
from friday_engine.config import LLMConfig
from friday_engine.llm.base import (
    BaseLLMProvider,
    LLMError,
    LLMMessage,
    LLMResponse,
    Role,
)
from friday_engine.llm.claude_provider import ClaudeProvider
from friday_engine.llm.gemini_provider import GeminiProvider
from friday_engine.llm.local_provider import LocalLLMProvider
from friday_engine.llm.openai_provider import OpenAIProvider
from friday_engine.logger import logger


class LLMRouter:
    """
    Intelligent router for LLM calls with priority fallback.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.priority: List[str] = list(self.config.priority)
        self._initialize_providers()

    def _initialize_providers(self) -> None:
        """Instantiate configured providers based on config values."""
        # 1. Gemini
        self.providers["gemini"] = GeminiProvider(
            api_key=self.config.gemini.api_key,
            model=self.config.gemini.model,
            timeout=self.config.gemini.timeout,
            temperature=self.config.gemini.temperature,
        )

        # 2. Claude
        self.providers["claude"] = ClaudeProvider(
            api_key=self.config.claude.api_key,
            model=self.config.claude.model,
            timeout=self.config.claude.timeout,
            temperature=self.config.claude.temperature,
        )

        # 3. OpenAI
        self.providers["openai"] = OpenAIProvider(
            api_key=self.config.openai.api_key,
            model=self.config.openai.model,
            base_url=self.config.openai.base_url,
            timeout=self.config.openai.timeout,
            temperature=self.config.openai.temperature,
        )

        # 4. Local
        self.providers["local"] = LocalLLMProvider(
            base_url=self.config.local.base_url,
            model=self.config.local.model,
            timeout=self.config.local.timeout,
            temperature=self.config.local.temperature,
        )

    def register_provider(self, name: str, provider: BaseLLMProvider, priority_index: Optional[int] = None) -> None:
        """Dynamically add or replace a provider in the router."""
        self.providers[name] = provider
        if name not in self.priority:
            if priority_index is not None:
                self.priority.insert(priority_index, name)
            else:
                self.priority.append(name)
        logger.info(f"Registered custom LLM provider '{name}'. Priority order: {self.priority}")

    async def chat(
        self,
        messages: Union[str, List[LLMMessage]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        preferred_provider: Optional[str] = None,
        **kwargs,
    ) -> LLMResponse:
        """
        Send chat prompt to providers following priority order with automatic fallback.
        """
        if isinstance(messages, str):
            msg_list = [LLMMessage(role=Role.USER, content=messages)]
        else:
            msg_list = messages

        order: List[str] = []
        if preferred_provider and preferred_provider in self.providers:
            order.append(preferred_provider)
        for p in self.priority:
            if p not in order and p in self.providers:
                order.append(p)

        last_error: Optional[Exception] = None

        for provider_name in order:
            provider = self.providers.get(provider_name)
            if not provider:
                continue

            try:
                logger.debug(f"Attempting inference via [{provider_name}] (model: {provider.model})...")
                response = await provider.chat(
                    messages=msg_list,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                logger.debug(
                    f"Inference succeeded via [{provider_name}] in {response.latency_seconds:.2f}s "
                    f"({response.output_tokens} output tokens)."
                )
                return response
            except Exception as exc:
                last_error = exc
                logger.warning(
                    f"Provider [{provider_name}] failed: {exc}. "
                    f"Attempting fallback to next provider in queue..."
                )
                continue

        error_msg = f"All LLM backends ({order}) failed. Last exception: {last_error}"
        logger.error(error_msg)
        raise LLMError(error_msg) from last_error

    async def generate(self, prompt: str, **kwargs) -> str:
        """Helper to get string response directly."""
        resp = await self.chat(prompt, **kwargs)
        return resp.content
