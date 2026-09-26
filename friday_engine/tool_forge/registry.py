"""
F.R.I.D.A.Y. Dynamic Tool Registry.
Registers, discovers, schemas, and executes dynamic and built-in tools.
"""

from __future__ import annotations

import inspect
import time
from typing import Any, Callable, Dict, List, Optional
from friday_engine.logger import logger
from friday_engine.tool_forge.models import ToolDefinition, ToolExecutionResult


class ToolRegistry:
    """
    Registry of live tools available to F.R.I.D.A.Y.
    """

    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._definitions: Dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        definition: Optional[ToolDefinition] = None,
    ) -> None:
        """Register a callable tool with its definition schema."""
        self._tools[name] = handler
        if definition:
            self._definitions[name] = definition
        else:
            # Auto-generate definition from function signature
            doc = inspect.getdoc(handler) or "No description provided."
            self._definitions[name] = ToolDefinition(name=name, description=doc)

        logger.info(f"Loaded dynamic tool: [{name}]")

    def unregister(self, name: str) -> bool:
        """Remove a tool from the active registry."""
        if name in self._tools:
            del self._tools[name]
            self._definitions.pop(name, None)
            logger.info(f"Unregistered tool: [{name}]")
            return True
        return False

    def get_tool(self, name: str) -> Optional[Callable[..., Any]]:
        return self._tools.get(name)

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def get_all_tools(self) -> Dict[str, Callable[..., Any]]:
        return self._tools

    def get_definition(self, name: str) -> Optional[ToolDefinition]:
        return self._definitions.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of all registered tools with MCP-compatible metadata."""
        output = []
        for name, defn in self._definitions.items():
            output.append({
                "name": name,
                "description": defn.description,
                "parameters": [p.model_dump() for p in defn.parameters],
                "version": defn.version,
            })
        return output

    async def execute(self, name: str, **kwargs) -> ToolExecutionResult:
        """Execute a tool safely and return structured execution result."""
        tool = self._tools.get(name)
        if not tool:
            return ToolExecutionResult(
                success=False,
                error=f"Tool '{name}' is not registered in Friday Tool Registry.",
            )

        start = time.perf_counter()
        try:
            if inspect.iscoroutinefunction(tool):
                res = await tool(**kwargs)
            else:
                res = tool(**kwargs)
            latency = time.perf_counter() - start
            return ToolExecutionResult(success=True, data=res, execution_time_seconds=latency)
        except Exception as exc:
            latency = time.perf_counter() - start
            logger.error(f"Error executing tool '{name}': {exc}", exc_info=True)
            return ToolExecutionResult(
                success=False,
                error=str(exc),
                execution_time_seconds=latency,
            )
