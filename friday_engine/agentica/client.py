"""
F.R.I.D.A.Y. Agentica MCP Client.
Provides asynchronous interface to Agentica Browser MCP Server
for web automation, page navigation, form interactions, screenshots, and scraping.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional
import httpx

from friday_engine.config import AgenticaConfig
from friday_engine.logger import logger


class AgenticaError(Exception):
    """Base exception for Agentica client errors."""
    pass


class AgenticaClient:
    """
    Async client for communicating with Agentica MCP Server over HTTP JSON-RPC.
    """

    def __init__(self, config: Optional[AgenticaConfig] = None):
        self.config = config or AgenticaConfig()
        self.endpoint = self.config.endpoint.rstrip("/")
        self.timeout = self.config.timeout
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _rpc_call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a JSON-RPC 2.0 call to the Agentica server."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._next_id(),
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(f"{self.endpoint}/mcp", json=payload)
                if resp.status_code == 204:
                    return None
                if resp.status_code != 200:
                    raise AgenticaError(f"HTTP error {resp.status_code} from Agentica: {resp.text}")

                data = resp.json()
                if "error" in data:
                    raise AgenticaError(f"Agentica RPC Error: {data['error']}")
                result = data.get("result", {})
                
                # Check for MCP tool call error
                if result.get("isError"):
                    content = result.get("content", [{"text": "Unknown error"}])
                    raise AgenticaError(f"Tool Error: {content[0].get('text')}")
                
                # Extract text content from MCP response
                content = result.get("content", [])
                if content and len(content) > 0:
                    import json
                    text = content[0].get("text", "")
                    try:
                        return json.loads(text)
                    except:
                        return text
                return result
        except httpx.ConnectError as exc:
            raise AgenticaError(f"Could not connect to Agentica server at {self.endpoint}: {exc}") from exc
        except httpx.TimeoutException as exc:
            raise AgenticaError(f"Agentica request timed out after {self.timeout}s: {exc}") from exc

    async def health_check(self) -> bool:
        """Check if Agentica server is alive and responding."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.endpoint}/health")
                return resp.status_code == 200
        except Exception:
            return False

    async def browse(self, url: str, mode: str = "auto") -> Any:
        """Navigate to a specified URL."""
        logger.info(f"Agentica browsing to: {url} (mode: {mode})")
        return await self._rpc_call("tools/call", {"name": "browse", "arguments": {"url": url, "mode": mode}})

    async def snapshot(self, mode: str = "axtree") -> Any:
        """Capture DOM snapshot or pruned interactive tree."""
        return await self._rpc_call("tools/call", {"name": "snapshot", "arguments": {"mode": mode}})

    async def click(self, selector_or_ref: str) -> Any:
        """Click an element on the page."""
        logger.info(f"Agentica clicking: {selector_or_ref}")
        return await self._rpc_call("tools/call", {"name": "click", "arguments": {"ref": selector_or_ref}})

    async def type_text(self, selector_or_ref: str, text: str) -> Any:
        """Type text into an input field."""
        logger.info(f"Agentica typing into: {selector_or_ref}")
        return await self._rpc_call("tools/call", {"name": "fill", "arguments": {"ref": selector_or_ref, "text": text}})

    async def capture(self, url: str) -> Any:
        """Capture screenshot of the active view."""
        return await self._rpc_call("tools/call", {"name": "screenshot", "arguments": {"url": url}})

    async def act(self, action: str) -> Any:
        """Perform a natural language action."""
        logger.info(f"Agentica act: {action}")
        return await self._rpc_call("tools/call", {"name": "act", "arguments": {"action": action}})

    async def extract(self, prompt: str) -> Any:
        """Extract data based on natural language prompt."""
        logger.info(f"Agentica extract: {prompt}")
        return await self._rpc_call("tools/call", {"name": "extract", "arguments": {"prompt": prompt}})

    async def observe(self) -> Any:
        """Observe the current page state (pruned DOM + screenshot)."""
        logger.info(f"Agentica observing page state")
        return await self._rpc_call("tools/call", {"name": "observe", "arguments": {}})

