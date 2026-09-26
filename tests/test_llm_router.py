"""
Unit tests for Multi-LLM Router failover mechanics.
"""

from typing import List, Optional
import pytest
from friday_engine.config import LLMConfig
from friday_engine.llm.base import BaseLLMProvider, LLMError, LLMMessage, LLMResponse
from friday_engine.llm.router import LLMRouter


class MockFailingProvider(BaseLLMProvider):
    def __init__(self, name: str):
        super().__init__(name=name, model="mock-fail")

    async def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        raise LLMError(f"Mock failure from {self.name}")

    async def health_check(self) -> bool:
        return False


class MockWorkingProvider(BaseLLMProvider):
    def __init__(self, name: str, response_text: str):
        super().__init__(name=name, model="mock-success")
        self.response_text = response_text

    async def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        return LLMResponse(
            content=self.response_text,
            provider=self.name,
            model=self.model,
            latency_seconds=0.01,
        )

    async def health_check(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_llm_router_fallback():
    router = LLMRouter(LLMConfig(priority=["failing_provider", "backup_provider"]))
    router.register_provider("failing_provider", MockFailingProvider("failing_provider"), priority_index=0)
    router.register_provider("backup_provider", MockWorkingProvider("backup_provider", "Hello from backup!"), priority_index=1)

    response = await router.chat("Ping")
    assert response.provider == "backup_provider"
    assert response.content == "Hello from backup!"
