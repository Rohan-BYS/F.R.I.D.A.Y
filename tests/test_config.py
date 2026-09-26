"""
Unit tests for F.R.I.D.A.Y. configuration loading and validation.
"""

from pathlib import Path
import pytest
from friday_engine.config import FridayConfig, load_config


def test_default_config_loading():
    config = load_config()
    assert isinstance(config, FridayConfig)
    assert config.system.name == "F.R.I.D.A.Y."
    assert config.system.creator == "Rohan"
    assert "gemini" in config.llm.priority
    assert config.tool_forge.enabled is True
    assert config.midnight_protocol.schedule_time == "00:00"


def test_config_validation():
    data = {
        "system": {"name": "TestForge", "creator": "Rohan"},
        "llm": {"priority": ["claude", "gemini"]},
    }
    cfg = FridayConfig.model_validate(data)
    assert cfg.system.name == "TestForge"
    assert cfg.llm.priority == ["claude", "gemini"]
