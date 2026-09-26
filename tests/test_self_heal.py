"""
Unit tests for Self-Healing Diagnostics & AutoPatcher.
"""

import tempfile
from pathlib import Path
import pytest
from friday_engine.aci.code_surgeon import CodeSurgeon
from friday_engine.self_heal.auto_patcher import AutoPatcher
from friday_engine.self_heal.diagnostic import SelfHealingDiagnostic


def test_self_healing_traceback_diagnosis():
    sample_traceback = """
Traceback (most recent call last):
  File "C:/Users/U1/project/calculator.py", line 42, in compute
    result = 10 / 0
ZeroDivisionError: division by zero
"""
    diag = SelfHealingDiagnostic.diagnose(sample_traceback)
    assert diag.exception_type == "ZeroDivisionError"
    assert "calculator.py" in diag.file_path
    assert diag.line_number == 42
    assert diag.problem_code == "result = 10 / 0"
    assert diag.remediation_strategy == "CODE_SURGERY"


def test_self_healing_missing_package_diagnosis():
    sample_err = "ModuleNotFoundError: No module named 'fastapi_extra'"
    diag = SelfHealingDiagnostic.diagnose(sample_err)
    assert diag.exception_type == "ModuleNotFoundError"
    assert diag.target_package == "fastapi_extra"
    assert diag.remediation_strategy == "INSTALL_PACKAGE"


def test_auto_patcher_pinpoints_surgery_target():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "app.py"
        test_file.write_text("def run():\n    pass\n", encoding="utf-8")

        traceback = f"""
Traceback (most recent call last):
  File "{test_file.as_posix()}", line 2, in run
    raise ValueError("Invalid state")
ValueError: Invalid state
"""
        patcher = AutoPatcher()
        result = patcher.attempt_repair(traceback)
        assert result.success is True
        assert result.action_taken == "DIAGNOSED_FOR_SURGERY"
        assert result.diagnosis.line_number == 2
