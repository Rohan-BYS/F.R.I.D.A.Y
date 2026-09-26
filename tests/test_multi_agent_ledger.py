import pytest
import asyncio
from typing import Dict, Any

from friday_engine.config import FridayConfig
from friday_engine.core.engine import FridayEngine
from friday_engine.sub_agents.models import SubAgentTask, TaskResult, TaskStatus
from friday_engine.sub_agents.ledger import FactType

# Mock the subagent worker execution so we don't actually spawn real LLMs
async def mock_execute(task: SubAgentTask) -> TaskResult:
    await asyncio.sleep(0.1) # simulate work
    return TaskResult(
        task_id=task.task_id,
        status=TaskStatus.COMPLETED,
        output=f"Successfully completed: {task.goal}"
    )

@pytest.mark.asyncio
async def test_multi_agent_ledger_orchestration():
    config = FridayConfig()
    engine = FridayEngine(config)
    
    # Patch the worker pool's dispatch to use our mock executor
    original_dispatch = engine.pool.dispatch if hasattr(engine, 'pool') else engine.sub_agents.dispatch
    
    async def mock_dispatch(goal: str, payload: Dict[str, Any] = None):
        return await original_dispatch(goal, payload, executor_func=mock_execute)
        
    engine.sub_agents.dispatch = mock_dispatch
    
    goal = "Investigate the competitive landscape for F.R.I.D.A.Y."
    sub_tasks = [
        {"description": "Read documentation for Magentic-One", "assignee": "researcher"},
        {"description": "Analyze CrewAI source code", "assignee": "coder"},
        {"description": "Draft competitive analysis report", "assignee": "writer"}
    ]
    
    summary = await engine.delegate_task(global_goal=goal, sub_tasks=sub_tasks)
    
    assert "Global Goal: Investigate the competitive landscape" in summary
    assert "Status: Resolved" in summary
    assert "Read documentation for Magentic-One" in summary
    assert "Analyze CrewAI source code" in summary
    
    # Check that entries were added by the Orchestrator and the workers
    assert "DECISION] All sub-tasks completed. Goal achieved." in summary
