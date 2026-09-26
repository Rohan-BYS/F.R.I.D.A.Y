"""
Tool Forge Sandboxing and Automated Validation.
Verifies Python syntax via AST and runs unit tests in an isolated subprocess with timeouts.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Tuple, Optional
from friday_engine.logger import logger


class SandboxError(Exception):
    """Raised when sandbox validation or test execution fails."""
    pass


class ToolSandbox:
    """
    Executes sandboxed tests for dynamically generated tools.
    """

    def __init__(self, sandbox_dir: Optional[Path | str] = None, default_timeout: int = 15):
        self.sandbox_dir = Path(sandbox_dir) if sandbox_dir else Path(tempfile.gettempdir()) / "friday_forge_sandbox"
        self.default_timeout = default_timeout
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def validate_syntax(self, code: str) -> None:
        """Parse code into AST to detect syntax errors before execution."""
        try:
            ast.parse(code)
        except SyntaxError as exc:
            raise SandboxError(f"Syntax error on line {exc.lineno}: {exc.msg}") from exc

    def test_tool(self, tool_code: str, test_code: str, timeout: Optional[int] = None) -> Tuple[bool, str]:
        """
        Write tool and unit tests to sandbox directory, run unittest in a separate process,
        and return (success, test_output).
        """
        self.validate_syntax(tool_code)
        self.validate_syntax(test_code)

        run_timeout = timeout or self.default_timeout
        timestamp = int(time.time() * 1000)
        tool_file = self.sandbox_dir / f"tool_{timestamp}.py"
        test_file = self.sandbox_dir / f"test_tool_{timestamp}.py"

        # Embed import of the tool file into test
        adjusted_test_code = (
            f"import sys\n"
            f"sys.path.insert(0, r'{self.sandbox_dir}')\n"
            f"from tool_{timestamp} import *\n"
            f"{test_code}\n"
            f"if __name__ == '__main__':\n"
            f"    import unittest\n"
            f"    unittest.main()\n"
        )

        try:
            tool_file.write_text(tool_code, encoding="utf-8")
            test_file.write_text(adjusted_test_code, encoding="utf-8")

            # Run python process
            proc = subprocess.run(
                [sys.executable, str(test_file.resolve())],
                capture_output=True,
                text=True,
                timeout=run_timeout,
                cwd=str(self.sandbox_dir.resolve()),
            )

            success = proc.returncode == 0
            output = f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            if not success:
                logger.warning(f"Sandbox test failed for tool_{timestamp}:\n{output}")
            return success, output

        except subprocess.TimeoutExpired:
            return False, f"Test execution timed out after {run_timeout} seconds."
        except Exception as exc:
            return False, f"Sandbox error: {exc}"
        finally:
            # Clean up sandbox temp files
            try:
                if tool_file.exists():
                    tool_file.unlink()
                if test_file.exists():
                    test_file.unlink()
            except Exception:
                pass
