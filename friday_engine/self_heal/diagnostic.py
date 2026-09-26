"""
Self-Healing Diagnostic Engine.
Parses stack traces, unhandled exceptions, and log errors into actionable repair targets.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel


class DiagnosticDiagnosis(BaseModel):
    exception_type: str
    error_message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    problem_code: Optional[str] = None
    remediation_strategy: str  # 'INSTALL_PACKAGE', 'CODE_SURGERY', 'RETRY', 'UNKNOWN'
    target_package: Optional[str] = None


class SelfHealingDiagnostic:
    """
    Analyzes Python error outputs and determines the exact root cause.
    """

    TRACEBACK_PATTERN = re.compile(
        r'File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<func>\w+)\n\s*(?P<code>.+?)\n(?P<err>\w+Error|\w+Exception): (?P<msg>.+)',
        re.MULTILINE,
    )

    MODULE_MISSING_PATTERN = re.compile(r"No module named ['\"](?P<pkg>[^'\"]+)['\"]")

    @classmethod
    def diagnose(cls, error_text: str) -> DiagnosticDiagnosis:
        """Analyze traceback and classify remediation strategy."""
        clean_text = error_text.strip()

        # Check for missing package / dependency
        pkg_match = cls.MODULE_MISSING_PATTERN.search(clean_text)
        if pkg_match:
            pkg_name = pkg_match.group("pkg").split(".")[0]
            return DiagnosticDiagnosis(
                exception_type="ModuleNotFoundError",
                error_message=f"Missing module '{pkg_name}'",
                remediation_strategy="INSTALL_PACKAGE",
                target_package=pkg_name,
            )

        # Parse traceback frames
        matches = list(cls.TRACEBACK_PATTERN.finditer(clean_text))
        if matches:
            last_frame = matches[-1]
            return DiagnosticDiagnosis(
                exception_type=last_frame.group("err"),
                error_message=last_frame.group("msg").strip(),
                file_path=last_frame.group("file").strip(),
                line_number=int(last_frame.group("line")),
                problem_code=last_frame.group("code").strip(),
                remediation_strategy="CODE_SURGERY",
            )

        # Fallback heuristic
        lines = [ln.strip() for ln in clean_text.splitlines() if ln.strip()]
        last_line = lines[-1] if lines else "Unknown Error"

        return DiagnosticDiagnosis(
            exception_type="GenericError",
            error_message=last_line,
            remediation_strategy="UNKNOWN",
        )
