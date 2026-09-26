"""
Trajectory Evaluator for F.R.I.D.A.Y. Self-Evolution.
Grades execution results to decide whether to distill a workflow into a permanent skill.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel


class EvaluationResult(BaseModel):
    is_success: bool
    score: float  # 0.0 to 1.0
    reason: str
    suggested_skill_name: Optional[str] = None


class TrajectoryEvaluator:
    """
    Evaluates action outcomes and decides if they should become learned skills.
    """

    @staticmethod
    def evaluate_task_outcome(
        goal: str,
        output: Any,
        error: Optional[str] = None,
        execution_time: float = 0.0,
    ) -> EvaluationResult:
        if error:
            return EvaluationResult(
                is_success=False,
                score=0.0,
                reason=f"Execution raised error: {error}",
            )

        if not output:
            return EvaluationResult(
                is_success=False,
                score=0.2,
                reason="Task returned empty output.",
            )

        output_str = str(output).strip()
        if len(output_str) < 5:
            return EvaluationResult(
                is_success=False,
                score=0.4,
                reason="Output too brief to evaluate as skill.",
            )

        # Baseline heuristic score
        score = 0.85
        if execution_time > 0 and execution_time < 5.0:
            score += 0.1  # Fast execution bonus

        # Generate a suggested skill name from the goal
        clean_goal = "".join(c if c.isalnum() or c == " " else "" for c in goal)
        suggested_name = "_".join(clean_goal.lower().split()[:4])

        return EvaluationResult(
            is_success=True,
            score=min(score, 1.0),
            reason="Execution completed cleanly with verified non-empty output.",
            suggested_skill_name=suggested_name,
        )
