"""
F.R.I.D.A.Y. Self-Healing Subsystem.
Law 4 of Friday: The Law of Self-Healing.
"""

from friday_engine.self_heal.auto_patcher import AutoPatcher, PatchResult
from friday_engine.self_heal.diagnostic import (
    DiagnosticDiagnosis,
    SelfHealingDiagnostic,
)

__all__ = ["AutoPatcher", "PatchResult", "SelfHealingDiagnostic", "DiagnosticDiagnosis"]
