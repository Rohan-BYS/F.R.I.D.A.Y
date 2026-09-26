"""
F.R.I.D.A.Y. Skill Distiller.
Turns successful trajectories into robust, reusable Python tools and SKILL.md modules.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional
from friday_engine.evolution.evaluator import TrajectoryEvaluator
from friday_engine.evolution.skill_store import SkillStore
from friday_engine.logger import logger


class SkillDistiller:
    """
    Distills successful executions into permanent tools.
    """

    def __init__(self, skill_store: SkillStore):
        self.skill_store = skill_store
        self.evaluator = TrajectoryEvaluator()

    def distill_from_code(
        self,
        skill_name: str,
        description: str,
        python_code: str,
        test_code: Optional[str] = None,
        category: str = "automation",
    ) -> bool:
        """
        Validate and distill a Python script into a permanent skill.
        """
        # Basic validation: ensure code contains def
        if "def " not in python_code:
            logger.warning(f"Cannot distill skill '{skill_name}': Code contains no function definition.")
            return False

        return self.skill_store.save_skill(
            name=skill_name,
            description=description,
            code=python_code,
            test_code=test_code,
            category=category,
        )
