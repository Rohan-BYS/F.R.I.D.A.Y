"""
Unit tests for CodeSurgeon precision surgery engine (SWE-agent / Anthropic reverse-engineered).
"""

import tempfile
from pathlib import Path
import pytest
from friday_engine.aci.code_surgeon import CodeSurgeon


def test_code_surgeon_full_workflow():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "module.py"
        surgeon = CodeSurgeon()

        # 1. Create file
        initial_code = """import os

def calculate_tax(income: float) -> float:
    rate = 0.10
    return income * rate
"""
        res = surgeon.create_file(test_file, initial_code)
        assert res.success is True
        assert test_file.exists()

        # 2. View slice
        view_text = surgeon.view(test_file, start_line=3, end_line=5)
        assert "calculate_tax" in view_text
        assert "rate = 0.10" in view_text

        # 3. Surgical str_replace (modify rate to 0.15)
        res_edit = surgeon.str_replace(
            path=test_file,
            old_str="rate = 0.10",
            new_str="rate = 0.15",
        )
        assert res_edit.success is True
        assert res_edit.syntax_valid is True
        assert "rate = 0.15" in test_file.read_text(encoding="utf-8")

        # 4. AST Syntax Guard prevents broken syntax
        res_broken = surgeon.str_replace(
            path=test_file,
            old_str="rate = 0.15",
            new_str="rate = 0.15 (((broken syntax",
        )
        assert res_broken.success is False
        assert res_broken.syntax_valid is False
        # File should remain unmodified
        assert "rate = 0.15" in test_file.read_text(encoding="utf-8")

        # 5. Insert documentation line
        res_insert = surgeon.insert(
            path=test_file,
            line_number=3,
            text='    """Calculates income tax."""',
        )
        assert res_insert.success is True
        assert '"""Calculates income tax."""' in test_file.read_text(encoding="utf-8")

        # 6. Undo rollback
        res_undo = surgeon.undo(test_file)
        assert res_undo.success is True
        # Docstring should be rolled back
        assert '"""Calculates income tax."""' not in test_file.read_text(encoding="utf-8")
