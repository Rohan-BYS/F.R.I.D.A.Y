"""
F.R.I.D.A.Y. Code Surgeon (Agent-Computer Interface).
Reverse-engineered from SWE-agent (str_replace_editor) and Anthropic tools.
Performs surgical line-level code viewing, replacement, insertion, AST validation, and rollback.
"""

from __future__ import annotations

import ast
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field
from friday_engine.logger import logger


class SurgeryResult(BaseModel):
    success: bool
    message: str
    diff: Optional[str] = None
    old_str: Optional[str] = None
    new_str: Optional[str] = None
    syntax_valid: bool = True
    undo_available: bool = False


class CodeSurgeon:
    """
    Precision code editing engine preventing hallucinated rewrites.
    """

    def __init__(self):
        # In-memory undo history: path -> list of previous file contents
        self._history: Dict[str, List[str]] = {}

    def _get_history(self, path: Path) -> List[str]:
        resolved = str(path.resolve())
        if resolved not in self._history:
            self._history[resolved] = []
        return self._history[resolved]

    def _push_history(self, path: Path, content: str) -> None:
        hist = self._get_history(path)
        hist.append(content)
        # Keep maximum 20 historical revisions
        if len(hist) > 20:
            hist.pop(0)

    def validate_python_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax via AST without executing code."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as exc:
            return False, f"Line {exc.lineno}, Col {exc.offset}: {exc.msg}"

    def view(
        self,
        path: str | Path,
        start_line: int = 1,
        end_line: Optional[int] = None,
    ) -> str:
        """
        View a slice of a file with 1-indexed line numbers.
        """
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        total_lines = len(lines)

        start = max(1, start_line)
        stop = min(total_lines, end_line if end_line is not None else total_lines)

        if start > total_lines:
            return f"[Empty range: start line {start} exceeds total lines {total_lines}]"

        output = [f"--- File: {file_path} (Lines {start}-{stop} of {total_lines}) ---"]
        for idx in range(start, stop + 1):
            line_content = lines[idx - 1].rstrip("\r\n")
            output.append(f"{idx:5d} | {line_content}")

        return "\n".join(output)

    def create_file(self, path: str | Path, content: str, overwrite: bool = False) -> SurgeryResult:
        """Create a new file with parent directory auto-creation."""
        file_path = Path(path)
        if file_path.exists() and not overwrite:
            return SurgeryResult(
                success=False,
                message=f"File already exists at {file_path}. Set overwrite=True to replace.",
            )

        if file_path.suffix == ".py":
            valid, err = self.validate_python_syntax(content)
            if not valid:
                return SurgeryResult(
                    success=False,
                    message=f"Syntax validation failed: {err}",
                    syntax_valid=False,
                )

        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            self._push_history(file_path, file_path.read_text(encoding="utf-8", errors="replace"))

        file_path.write_text(content, encoding="utf-8")
        logger.info(f"CodeSurgeon created file: {file_path}")
        return SurgeryResult(success=True, message=f"Successfully created {file_path}")

    def str_replace(
        self,
        path: str | Path,
        old_str: str,
        new_str: str,
        validate_syntax: bool = True,
    ) -> SurgeryResult:
        """
        Replace an exact, unique occurrence of old_str with new_str.
        """
        file_path = Path(path)
        if not file_path.is_file():
            return SurgeryResult(success=False, message=f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8", errors="replace")

        # 1. Uniqueness check
        count = content.count(old_str)
        if count == 0:
            return SurgeryResult(
                success=False,
                message="Target 'old_str' not found in file. Ensure exact whitespace and linebreaks match.",
            )
        elif count > 1:
            return SurgeryResult(
                success=False,
                message=f"Target 'old_str' is not unique (found {count} occurrences). Include more surrounding context lines.",
            )

        # 2. Perform replacement
        new_content = content.replace(old_str, new_str, 1)

        # 3. Syntax validation for Python files
        if validate_syntax and file_path.suffix == ".py":
            is_valid, error_msg = self.validate_python_syntax(new_content)
            if not is_valid:
                return SurgeryResult(
                    success=False,
                    message=f"Replacement rejected by AST Syntax Guard: {error_msg}",
                    syntax_valid=False,
                )

        # 4. Generate unified diff
        diff = difflib.unified_diff(
            content.splitlines(),
            new_content.splitlines(),
            fromfile=f"a/{file_path.name}",
            tofile=f"b/{file_path.name}",
            lineterm="",
        )
        diff_text = "\n".join(diff)

        # 5. Save and record history for undo
        self._push_history(file_path, content)
        file_path.write_text(new_content, encoding="utf-8")
        logger.info(f"CodeSurgeon applied surgical replacement to {file_path}")

        return SurgeryResult(
            success=True,
            message=f"Successfully patched {file_path}",
            diff=diff_text,
            old_str=old_str,
            new_str=new_str,
            syntax_valid=True,
            undo_available=True,
        )

    def insert(
        self,
        path: str | Path,
        line_number: int,
        text: str,
        validate_syntax: bool = True,
    ) -> SurgeryResult:
        """
        Insert text immediately after line_number (1-indexed). 0 inserts at the beginning.
        """
        file_path = Path(path)
        if not file_path.is_file():
            return SurgeryResult(success=False, message=f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines(keepends=True)

        if line_number < 0 or line_number > len(lines):
            return SurgeryResult(
                success=False,
                message=f"Invalid line number {line_number}. File has {len(lines)} lines.",
            )

        insert_text = text if text.endswith("\n") else text + "\n"
        if line_number == 0:
            new_lines = [insert_text] + lines
        else:
            new_lines = lines[:line_number] + [insert_text] + lines[line_number:]

        new_content = "".join(new_lines)

        if validate_syntax and file_path.suffix == ".py":
            is_valid, error_msg = self.validate_python_syntax(new_content)
            if not is_valid:
                return SurgeryResult(
                    success=False,
                    message=f"Insertion rejected by AST Syntax Guard: {error_msg}",
                    syntax_valid=False,
                )

        diff = difflib.unified_diff(
            content.splitlines(),
            new_content.splitlines(),
            fromfile=f"a/{file_path.name}",
            tofile=f"b/{file_path.name}",
            lineterm="",
        )
        diff_text = "\n".join(diff)

        self._push_history(file_path, content)
        file_path.write_text(new_content, encoding="utf-8")
        logger.info(f"CodeSurgeon inserted text at line {line_number} in {file_path}")

        return SurgeryResult(
            success=True,
            message=f"Successfully inserted lines at line {line_number}",
            diff=diff_text,
            undo_available=True,
        )

    def undo(self, path: str | Path) -> SurgeryResult:
        """Roll back file to its state before the last edit."""
        file_path = Path(path)
        hist = self._get_history(file_path)
        if not hist:
            return SurgeryResult(success=False, message="No undo history available for this file.")

        previous_content = hist.pop()
        current_content = file_path.read_text(encoding="utf-8", errors="replace")

        diff = difflib.unified_diff(
            current_content.splitlines(),
            previous_content.splitlines(),
            fromfile=f"a/{file_path.name}",
            tofile=f"b/{file_path.name} (rollback)",
            lineterm="",
        )
        file_path.write_text(previous_content, encoding="utf-8")
        logger.info(f"CodeSurgeon rolled back {file_path} to previous revision.")

        return SurgeryResult(
            success=True,
            message=f"Rollback successful for {file_path}",
            diff="\n".join(diff),
            undo_available=bool(hist),
        )
