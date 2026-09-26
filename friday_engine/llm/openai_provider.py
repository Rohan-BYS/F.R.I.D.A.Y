"""
OpenAI & Compatible LLM Provider.
Works with OpenAI, Groq, Ollama, DeepSeek, vLLM, and any OpenAI-compatible API.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
import httpx

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
from friday_engine.logger import logger


class OpenAIProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 30,
        temperature: float = 0.2,
    ):
        super().__init__(name="openai", model=model, timeout=timeout)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        temp = temperature if temperature is not None else self.temperature
        payload_messages = []
        for msg in messages:
            role = str(msg.role.value if isinstance(msg.role, Role) else msg.role).lower()
            payload_messages.append({"role": role, "content": msg.content})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": payload_messages,
            "temperature": temp,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(url, headers=headers, json=payload)
            except httpx.TimeoutException as exc:
                self.record_failure()
                raise LLMTimeoutError(f"OpenAI request timed out: {exc}") from exc
            except httpx.RequestError as exc:
                self.record_failure()
                raise LLMError(f"OpenAI network request error: {exc}") from exc

        latency = time.perf_counter() - start_time

        if resp.status_code == 401 or resp.status_code == 403:
            self.record_failure()
            raise LLMAuthenticationError(f"OpenAI authentication failed: {resp.text}")
        elif resp.status_code == 429:
            self.record_failure()
            raise LLMRateLimitError(f"OpenAI rate limit exceeded: {resp.text}")
        elif resp.status_code != 200:
            self.record_failure()
            raise LLMError(f"OpenAI API returned status {resp.status_code}: {resp.text}")

        data = resp.json()
        self.record_success()

        choices = data.get("choices", [])
        if not choices:
            return LLMResponse(
                content="",
                provider=self.name,
                model=self.model,
                raw_response=data,
                latency_seconds=latency,
            )

        first_choice = choices[0]
        text = first_choice.get("message", {}).get("content", "")
        finish_reason = first_choice.get("finish_reason")

        usage = data.get("usage", {})
        return LLMResponse(
            content=text,
            provider=self.name,
            model=self.model,
            raw_response=data,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            latency_seconds=latency,
            finish_reason=finish_reason,
        )

    async def health_check(self) -> bool:
        try:
            res = await self.chat([LLMMessage(role=Role.USER, content="ping")], max_tokens=2)
            return bool(res.content)
        except Exception as exc:
            logger.debug(f"OpenAI health check failed: {exc}")
            return False
