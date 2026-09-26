"""
Unit tests for Self-Evolution & Skill Learning loop.
"""

import tempfile
from pathlib import Path
import pytest
from friday_engine.evolution.distiller import SkillDistiller
from friday_engine.evolution.evaluator import TrajectoryEvaluator
from friday_engine.evolution.skill_store import SkillStore
from friday_engine.memory.sqlite_wal import DatabaseConnectionPool
from friday_engine.tool_forge.forge import ToolForge
from friday_engine.tool_forge.registry import ToolRegistry


def test_skill_store_and_distillation():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_evo.db"
        skills_dir = Path(temp_dir) / "skills"
        tools_dir = Path(temp_dir) / "custom_tools"
        sandbox_dir = Path(temp_dir) / "sandbox"

        pool = DatabaseConnectionPool(db_path)
        # Ensure schema
        from friday_engine.memory.fts_index import ensure_fts_schema
        ensure_fts_schema(pool.get_connection())

        from friday_engine.config import ToolForgeConfig
        forge_cfg = ToolForgeConfig(
            sandbox_dir=str(sandbox_dir),
            generated_tools_dir=str(tools_dir),
            test_timeout_seconds=5,
        )
        registry = ToolRegistry()
        forge = ToolForge(config=forge_cfg, registry=registry)

        skill_store = SkillStore(pool=pool, skills_dir=skills_dir, forge=forge)
        distiller = SkillDistiller(skill_store)

        skill_code = """
def calculate_vat(amount: float, rate: float = 0.20) -> float:
    return amount * rate
"""
        test_code = """
import unittest

class TestVAT(unittest.TestCase):
    def test_vat(self):
        res = calculate_vat(100.0, 0.20)
        self.assertAlmostEqual(res, 20.0)
"""

        # Distill skill
        success = distiller.distill_from_code(
            skill_name="calculate_vat",
            description="Computes Value Added Tax for a given amount.",
            python_code=skill_code,
            test_code=test_code,
            category="finance",
        )
        assert success is True

        # Verify SQLite record
        skill_record = skill_store.get_skill("calculate_vat")
        assert skill_record is not None
        assert skill_record["name"] == "calculate_vat"
        assert skill_record["category"] == "finance"

        # Verify SKILL.md file creation
        skill_md_path = skills_dir / "calculate_vat" / "SKILL.md"
        assert skill_md_path.exists()
        assert "calculate_vat" in skill_md_path.read_text(encoding="utf-8")

        # Verify FTS search
        search_hits = skill_store.search_skills("Value Added Tax")
        assert len(search_hits) >= 1
        assert search_hits[0]["name"] == "calculate_vat"

        # Verify hot-loaded into active ToolForge registry
        fn = registry.get_tool("calculate_vat")
        assert fn is not None
        assert fn(200.0, 0.15) == 30.0

        pool.close()


def test_trajectory_evaluator():
    evaluator = TrajectoryEvaluator()
    res = evaluator.evaluate_task_outcome(
        goal="scrape 100 stock quotes",
        output="Successfully parsed 100 tickers with metadata.",
        execution_time=1.2,
    )
    assert res.is_success is True
    assert res.score >= 0.8
    assert res.suggested_skill_name == "scrape_100_stock_quotes"
