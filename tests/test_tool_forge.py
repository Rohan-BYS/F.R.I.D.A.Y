"""
Unit tests for dynamic Tool Forge code generation and sandboxed verification.
"""

import tempfile
from pathlib import Path
import pytest
from friday_engine.config import ToolForgeConfig
from friday_engine.tool_forge.forge import ToolForge
from friday_engine.tool_forge.models import ToolDefinition
from friday_engine.tool_forge.registry import ToolRegistry
from friday_engine.tool_forge.sandbox import SandboxError


def test_tool_forge_synthesis_and_execution():
    with tempfile.TemporaryDirectory() as temp_dir:
        sandbox_dir = Path(temp_dir) / "sandbox"
        tools_dir = Path(temp_dir) / "tools"

        cfg = ToolForgeConfig(
            sandbox_dir=str(sandbox_dir),
            generated_tools_dir=str(tools_dir),
            test_timeout_seconds=5,
        )
        registry = ToolRegistry()
        forge = ToolForge(config=cfg, registry=registry)

        tool_code = """
def compute_profit_margin(revenue: float, cost: float) -> float:
    if revenue <= 0:
        return 0.0
    return ((revenue - cost) / revenue) * 100.0
"""
        test_code = """
import unittest

class TestProfit(unittest.TestCase):
    def test_margin(self):
        res = compute_profit_margin(100.0, 70.0)
        self.assertAlmostEqual(res, 30.0)
"""

        tool_def = ToolDefinition(
            name="compute_profit_margin",
            description="Computes business profit margin percentage.",
            code=tool_code,
            test_code=test_code,
        )

        success = forge.synthesize_tool(tool_def)
        assert success is True

        # Tool must now be in registry
        tool_fn = registry.get_tool("compute_profit_margin")
        assert tool_fn is not None
        assert tool_fn(200.0, 150.0) == 25.0


def test_tool_forge_catches_failing_test():
    with tempfile.TemporaryDirectory() as temp_dir:
        sandbox_dir = Path(temp_dir) / "sandbox"
        tools_dir = Path(temp_dir) / "tools"

        cfg = ToolForgeConfig(
            sandbox_dir=str(sandbox_dir),
            generated_tools_dir=str(tools_dir),
            test_timeout_seconds=5,
        )
        forge = ToolForge(config=cfg)

        broken_code = """
def broken_fn():
    return False
"""
        failing_test = """
import unittest
class TestFailing(unittest.TestCase):
    def test_must_fail(self):
        self.assertTrue(broken_fn())
"""
        tool_def = ToolDefinition(
            name="broken_tool",
            description="A broken tool that must fail validation.",
            code=broken_code,
            test_code=failing_test,
        )

        with pytest.raises(SandboxError):
            forge.synthesize_tool(tool_def)
