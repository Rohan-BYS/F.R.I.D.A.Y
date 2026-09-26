"""
F.R.I.D.A.Y. Verified Terminal (Agent-Computer Interface).
Reverse-engineered from OpenHands command execution and observation verification loop.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from friday_engine.logger import logger


class CommandObservation(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    execution_time_seconds: float
    is_success: bool
    error_category: Optional[str] = None
    summary: str


class VerifiedTerminal:
    """
    Subprocess execution environment with structured observation analysis.
    """

    def __init__(self, default_timeout: int = 60, working_dir: Optional[str | Path] = None, use_docker: bool = False, container_name: str = "friday_sandbox"):
        self.default_timeout = default_timeout
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self.use_docker = use_docker
        self.container_name = container_name

    def _classify_error(self, stderr: str, stdout: str) -> Optional[str]:
        combined = f"{stdout}\n{stderr}"
        if "ModuleNotFoundError" in combined or "No module named" in combined:
            return "MISSING_DEPENDENCY"
        elif "SyntaxError" in combined:
            return "SYNTAX_ERROR"
        elif "ImportError" in combined:
            return "IMPORT_ERROR"
        elif "PermissionError" in combined or "Access is denied" in combined:
            return "PERMISSION_DENIED"
        elif "FileNotFoundError" in combined or "cannot find the file" in combined:
            return "FILE_NOT_FOUND"
        elif "AssertionError" in combined or "FAILED (failures=" in combined or "FAILED (errors=" in combined:
            return "TEST_FAILURE"
        elif "command not found" in combined.lower() or "is not recognized as an internal or external command" in combined.lower():
            return "COMMAND_NOT_FOUND"
        return None

    def execute(
        self,
        command: str,
        timeout: Optional[int] = None,
        cwd: Optional[str | Path] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> CommandObservation:
        """
        Execute a shell command with strict timeout, output capture, and error classification.
        """
        run_cwd = Path(cwd) if cwd else self.working_dir
        run_timeout = timeout or self.default_timeout
        start_time = time.perf_counter()

        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)

        logger.info(f"VerifiedTerminal executing: {command} in {run_cwd}")

        try:
            if self.use_docker:
                docker_cmd = [
                    "docker", "exec", "-w", str(run_cwd), self.container_name,
                    "sh", "-c", command
                ]
                proc = subprocess.run(
                    docker_cmd,
                    capture_output=True,
                    timeout=run_timeout,
                    env=merged_env,
                )
            else:
                # Use PowerShell on Windows or bash/sh on Unix
                if sys.platform == "win32":
                    proc = subprocess.run(
                        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                        cwd=str(run_cwd),
                        capture_output=True,
                        timeout=run_timeout,
                        env=merged_env,
                    )
                else:
                    proc = subprocess.run(
                        command,
                        shell=True,
                        cwd=str(run_cwd),
                        capture_output=True,
                        timeout=run_timeout,
                        env=merged_env,
                    )

            elapsed = time.perf_counter() - start_time
            stdout = proc.stdout.decode("utf-8", errors="replace").strip()
            stderr = proc.stderr.decode("utf-8", errors="replace").strip()
            exit_code = proc.returncode
            is_success = (exit_code == 0)

            error_cat = self._classify_error(stderr=stderr, stdout=stdout) if not is_success else None

            if is_success:
                summary = f"Command succeeded in {elapsed:.2f}s (Exit code 0)"
            else:
                summary = f"Command failed with exit code {exit_code} (Category: {error_cat or 'UNKNOWN'})"

            logger.info(f"VerifiedTerminal result: {summary}")

            return CommandObservation(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                execution_time_seconds=elapsed,
                is_success=is_success,
                error_category=error_cat,
                summary=summary,
            )

        except subprocess.TimeoutExpired:
            elapsed = time.perf_counter() - start_time
            logger.error(f"Command timed out after {run_timeout}s: {command}")
            return CommandObservation(
                command=command,
                exit_code=-1,
                stdout="",
                stderr=f"Execution timed out after {run_timeout} seconds.",
                execution_time_seconds=elapsed,
                is_success=False,
                error_category="TIMEOUT",
                summary=f"Command timed out after {run_timeout}s",
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            logger.error(f"Command execution error: {exc}", exc_info=True)
            return CommandObservation(
                command=command,
                exit_code=-2,
                stdout="",
                stderr=str(exc),
                execution_time_seconds=elapsed,
                is_success=False,
                error_category="EXECUTION_EXCEPTION",
                summary=f"Execution error: {exc}",
            )
