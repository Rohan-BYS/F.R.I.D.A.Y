"""
Unit tests for VerifiedTerminal (OpenHands ACI command execution and observation).
"""

import sys
import pytest
from friday_engine.aci.terminal import VerifiedTerminal


def test_verified_terminal_success():
    term = VerifiedTerminal()
    obs = term.execute("Write-Output 'FRIDAY_ONLINE'" if sys.platform == "win32" else "echo 'FRIDAY_ONLINE'")
    assert obs.is_success is True
    assert obs.exit_code == 0
    assert "FRIDAY_ONLINE" in obs.stdout
    assert obs.execution_time_seconds >= 0.0


def test_verified_terminal_error_classification():
    term = VerifiedTerminal()
    # Execute python code with deliberate missing module
    cmd = 'python -c "import non_existent_super_module_xyz"'
    obs = term.execute(cmd)
    assert obs.is_success is False
    assert obs.exit_code != 0
    assert obs.error_category == "MISSING_DEPENDENCY"


def test_verified_terminal_timeout():
    term = VerifiedTerminal(default_timeout=2)
    # Command that sleeps longer than timeout
    sleep_cmd = "Start-Sleep -Seconds 4" if sys.platform == "win32" else "sleep 4"
    obs = term.execute(sleep_cmd)
    assert obs.is_success is False
    assert obs.error_category == "TIMEOUT"
