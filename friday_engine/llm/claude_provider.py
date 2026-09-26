"""
Anthropic Claude LLM Provider.
Integrates with Anthropic Messages API using httpx.
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


class ClaudeProvider(BaseLLMProvider):
    BASE_URL = "https://api.anthropic.com/v1/messages"

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        timeout: int = 30,
        temperature: float = 0.2,
    ):
        super().__init__(name="claude", model=model, timeout=timeout)
        self.api_key = api_key
        self.temperature = temperature

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        if not self.api_key:
            raise LLMAuthenticationError("Anthropic API key is not configured.")

        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens or 4096

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        system_prompt = ""
        claude_messages = []

        for msg in messages:
            role = str(msg.role.value if isinstance(msg.role, Role) else msg.role).lower()
            if role == "system":
                system_prompt += msg.content + "\n"
            elif role in ("user", "human"):
                claude_messages.append({"role": "user", "content": msg.content})
            elif role in ("assistant", "model"):
                claude_messages.append({"role": "assistant", "content": msg.content})
            else:
                claude_messages.append({"role": "user", "content": f"[{role.upper()}] {msg.content}"})

        if not claude_messages:
            claude_messages.append({"role": "user", "content": "Hello"})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": claude_messages,
            "max_tokens": tokens,
            "temperature": temp,
        }
        if system_prompt.strip():
            payload["system"] = system_prompt.strip()

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(self.BASE_URL, headers=headers, json=payload)
            except httpx.TimeoutException as exc:
                self.record_failure()
                raise LLMTimeoutError(f"Claude request timed out: {exc}") from exc
            except httpx.RequestError as exc:
                self.record_failure()
                raise LLMError(f"Claude network request error: {exc}") from exc

        latency = time.perf_counter() - start_time

        if resp.status_code == 401:
            self.record_failure()
            raise LLMAuthenticationError(f"Claude authentication failed: {resp.text}")
        elif resp.status_code == 429:
            self.record_failure()
            raise LLMRateLimitError(f"Claude rate limit exceeded: {resp.text}")
        elif resp.status_code != 200:
            self.record_failure()
            raise LLMError(f"Claude API returned error {resp.status_code}: {resp.text}")

        data = resp.json()
        self.record_success()

        # Parse content blocks
        blocks = data.get("content", [])
        text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        usage = data.get("usage", {})

        return LLMResponse(
            content=text,
            provider=self.name,
            model=self.model,
            raw_response=data,
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            latency_seconds=latency,
            finish_reason=data.get("stop_reason"),
        )

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            res = await self.chat([LLMMessage(role=Role.USER, content="ping")], max_tokens=2)
            return bool(res.content)
        except Exception as exc:
            logger.debug(f"Claude health check failed: {exc}")
            return False
