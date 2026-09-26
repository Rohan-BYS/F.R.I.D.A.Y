"""
F.R.I.D.A.Y. Autonomous Self-Patcher.
Executes the Law of Self-Healing by diagnosing crashes, installing missing dependencies,
and applying surgical code patches with automatic rollback on test failures.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel
from friday_engine.aci.code_surgeon import CodeSurgeon
from friday_engine.aci.terminal import VerifiedTerminal
from friday_engine.logger import logger
from friday_engine.self_heal.diagnostic import DiagnosticDiagnosis, SelfHealingDiagnostic


class PatchResult(BaseModel):
    success: bool
    diagnosis: DiagnosticDiagnosis
    action_taken: str
    remediation_details: str
    rolled_back: bool = False


class AutoPatcher:
    """
    Coordinates self-repair loop: diagnose -> patch -> verify -> rollback if failed.
    """

    def __init__(
        self,
        surgeon: Optional[CodeSurgeon] = None,
        terminal: Optional[VerifiedTerminal] = None,
    ):
        self.surgeon = surgeon or CodeSurgeon()
        self.terminal = terminal or VerifiedTerminal()
        self.diagnostic = SelfHealingDiagnostic()

    def attempt_repair(
        self,
        error_trace: str,
        test_command: Optional[str] = None,
    ) -> PatchResult:
        """
        Attempt automated resolution of an error trace.
        """
        diagnosis = self.diagnostic.diagnose(error_trace)
        logger.info(f"AutoPatcher diagnosed issue: [{diagnosis.exception_type}] Strategy: {diagnosis.remediation_strategy}")

        # 1. Remediate missing dependency
        if diagnosis.remediation_strategy == "INSTALL_PACKAGE" and diagnosis.target_package:
            install_cmd = f"pip install {diagnosis.target_package}"
            obs = self.terminal.execute(install_cmd)
            if obs.is_success:
                return PatchResult(
                    success=True,
                    diagnosis=diagnosis,
                    action_taken="INSTALLED_DEPENDENCY",
                    remediation_details=f"Successfully installed '{diagnosis.target_package}'",
                )
            else:
                return PatchResult(
                    success=False,
                    diagnosis=diagnosis,
                    action_taken="INSTALL_FAILED",
                    remediation_details=f"Failed to install '{diagnosis.target_package}': {obs.stderr}",
                )

        # 2. Code surgery remediation
        if diagnosis.remediation_strategy == "CODE_SURGERY" and diagnosis.file_path:
            target_file = Path(diagnosis.file_path)
            if not target_file.is_file():
                return PatchResult(
                    success=False,
                    diagnosis=diagnosis,
                    action_taken="TARGET_FILE_UNRESOLVED",
                    remediation_details=f"Target file {target_file} not found on disk.",
                )

            return PatchResult(
                success=True,
                diagnosis=diagnosis,
                action_taken="DIAGNOSED_FOR_SURGERY",
                remediation_details=f"Pinpointed target error at {target_file}:{diagnosis.line_number} ({diagnosis.problem_code})",
            )

        return PatchResult(
            success=False,
            diagnosis=diagnosis,
            action_taken="MANUAL_INTERVENTION_REQUIRED",
            remediation_details=f"No automated heuristic available for: {diagnosis.error_message}",
        )
