"""
Integration and bootstrap tests for the complete FridayEngine platform.
"""

import pytest
from friday_engine.core.engine import FridayEngine
from friday_engine.core.state import EngineStatus


@pytest.mark.asyncio
async def test_engine_initialization_and_boot():
    engine = FridayEngine()
    report = await engine.boot()

    assert report["version"] == "1.0.0"
    assert report["creator"] == "Rohan"
    assert engine.state.status == EngineStatus.READY

    # Verify all subsystems are attached and operational
    assert hasattr(engine, "llm")
    assert hasattr(engine, "vault")
    assert hasattr(engine, "forge")
    assert hasattr(engine, "agentica")
    assert hasattr(engine, "sub_agents")
    assert hasattr(engine, "midnight")

    # Verify subagent pool status
    pool_status = engine.sub_agents.get_status()
    assert pool_status["total_workers"] > 0
    assert pool_status["busy_workers"] == 0

    # Test dispatching a sub-agent task
    task_res = await engine.sub_agents.dispatch(
        goal="Test sub-goal execution",
        executor_func=lambda task: f"Completed: {task.goal}",
    )
    assert task_res.status.value == "completed"
    assert "Completed: Test sub-goal execution" in task_res.output

    # Shutdown
    await engine.shutdown()
    assert engine.state.status == EngineStatus.SHUTTING_DOWN
