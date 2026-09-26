"""
Google Gemini LLM Provider.
Integrates via Google Generative Language REST API (v1beta) using httpx.
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


class GeminiProvider(BaseLLMProvider):
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        timeout: int = 30,
        temperature: float = 0.2,
    ):
        super().__init__(name="gemini", model=model, timeout=timeout)
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
            raise LLMAuthenticationError("Gemini API key is not configured.")

        temp = temperature if temperature is not None else self.temperature
        url = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"

        # Convert messages to Gemini contents format
        contents = []
        system_instruction = None

        for msg in messages:
            role = str(msg.role.value if isinstance(msg.role, Role) else msg.role).lower()
            if role == "system":
                system_instruction = {"parts": [{"text": msg.content}]}
            elif role in ("user", "human"):
                contents.append({"role": "user", "parts": [{"text": msg.content}]})
            elif role in ("assistant", "model"):
                contents.append({"role": "model", "parts": [{"text": msg.content}]})
            else:
                contents.append({"role": "user", "parts": [{"text": f"[{role.upper()}] {msg.content}"}]})

        # Ensure at least one content block
        if not contents:
            contents.append({"role": "user", "parts": [{"text": "Hello"}]})

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temp,
            },
        }
        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens
        if system_instruction:
            payload["systemInstruction"] = system_instruction

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(url, json=payload)
            except httpx.TimeoutException as exc:
                self.record_failure()
                raise LLMTimeoutError(f"Gemini request timed out: {exc}") from exc
            except httpx.RequestError as exc:
                self.record_failure()
                raise LLMError(f"Gemini network request error: {exc}") from exc

        latency = time.perf_counter() - start_time

        if resp.status_code == 401 or resp.status_code == 403:
            self.record_failure()
            raise LLMAuthenticationError(f"Gemini authentication failed ({resp.status_code}): {resp.text}")
        elif resp.status_code == 429:
            self.record_failure()
            raise LLMRateLimitError(f"Gemini rate limit exceeded: {resp.text}")
        elif resp.status_code != 200:
            self.record_failure()
            raise LLMError(f"Gemini API returned error {resp.status_code}: {resp.text}")

        data = resp.json()
        self.record_success()

        # Parse text from candidate
        candidates = data.get("candidates", [])
        if not candidates:
            return LLMResponse(
                content="",
                provider=self.name,
                model=self.model,
                raw_response=data,
                latency_seconds=latency,
                finish_reason="no_candidates",
            )

        candidate = candidates[0]
        content_parts = candidate.get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in content_parts)
        finish_reason = candidate.get("finishReason")

        usage = data.get("usageMetadata", {})
        input_tokens = usage.get("promptTokenCount", 0)
        output_tokens = usage.get("candidatesTokenCount", 0)

        return LLMResponse(
            content=text,
            provider=self.name,
            model=self.model,
            raw_response=data,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_seconds=latency,
            finish_reason=finish_reason,
        )

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            test_msg = [LLMMessage(role=Role.USER, content="ping")]
            res = await self.chat(test_msg, max_tokens=2)
            return bool(res.content)
        except Exception as exc:
            logger.debug(f"Gemini health check failed: {exc}")
            return False
