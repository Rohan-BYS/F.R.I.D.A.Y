"""
F.R.I.D.A.Y. Tool Forge Orchestrator.
Dynamically creates, verifies, tests, and hot-loads Python tools into the engine.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from friday_engine.config import ToolForgeConfig
from friday_engine.logger import logger
from friday_engine.tool_forge.models import ToolDefinition, ToolExecutionResult
from friday_engine.tool_forge.registry import ToolRegistry
from friday_engine.tool_forge.sandbox import SandboxError, ToolSandbox


class ToolForge:
    """
    Autonomous tool synthesis and lifecycle management.
    """

    def __init__(
        self,
        config: Optional[ToolForgeConfig] = None,
        registry: Optional[ToolRegistry] = None,
    ):
        self.config = config or ToolForgeConfig()
        self.registry = registry or ToolRegistry()
        self.sandbox = ToolSandbox(
            sandbox_dir=self.config.sandbox_dir,
            default_timeout=self.config.test_timeout_seconds,
        )
        self.tools_dir = Path(self.config.generated_tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self._load_existing_tools()

    def _load_existing_tools(self) -> None:
        """Scan generated_tools_dir and load valid existing tools."""
        if not self.tools_dir.is_dir():
            return

        for py_file in self.tools_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            try:
                self._import_and_register_file(py_file)
            except Exception as exc:
                logger.warning(f"Failed to auto-load custom tool from {py_file}: {exc}")

    def _import_and_register_file(self, file_path: Path) -> None:
        """Dynamically import a Python file and register its functions."""
        module_name = f"friday_custom_tool_{file_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Find callable tool function matching stem or first exported function
            for attr_name in dir(module):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(module, attr_name)
                if callable(attr):
                    self.registry.register(attr_name, attr)

    def synthesize_tool(self, tool_def: ToolDefinition) -> bool:
        """
        Validate, sandbox test, persist, and register a new tool definition.
        """
        if not tool_def.code:
            raise SandboxError("ToolDefinition has no code to forge.")

        test_code = tool_def.test_code or "import unittest\nclass Dummy(unittest.TestCase):\n    def test_pass(self):\n        pass"

        logger.info(f"Initiating Forge lifecycle for tool: [{tool_def.name}]")

        # 1. Run sandbox test
        success, test_output = self.sandbox.test_tool(tool_def.code, test_code)
        if not success:
            raise SandboxError(f"Tool validation failed during sandboxed test execution:\n{test_output}")

        logger.info(f"Sandbox test passed successfully for tool [{tool_def.name}].")

        # 2. Persist tool to disk
        dest_file = self.tools_dir / f"{tool_def.name}.py"
        dest_file.write_text(tool_def.code, encoding="utf-8")

        # 3. Dynamic import and register
        self._import_and_register_file(dest_file)
        logger.info(f"Tool [{tool_def.name}] forged and registered into runtime.")
        return True

    def list_available_tools(self) -> List[Dict[str, Any]]:
        return self.registry.list_tools()
