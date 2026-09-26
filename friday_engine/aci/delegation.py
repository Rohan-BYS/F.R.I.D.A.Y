"""
F.R.I.D.A.Y. Specialist Agent Delegator.
Allows the main Engine to spawn isolated sub-agents powered by specific LLMs (e.g. Claude for coding).
"""

from typing import Dict, Any, Optional
from friday_engine.logger import logger
from friday_engine.llm.base import LLMMessage, Role

class SpecialistDelegator:
    """
    Spawns ephemeral sub-agents with specific model requirements to bypass rate limits
    and optimize for task-specific capabilities (coding, vision, logic).
    """
    def __init__(self, engine: Any):
        self.engine = engine

    async def spawn_specialist_agent(self, task: str, target_model: str, role_description: str = "Expert AI Agent") -> str:
        """
        Creates a new sub-agent for a specific task using a dedicated model.
        Available models: 'gemini', 'claude', 'openai', 'local'.
        Use this when a task is very heavy (like writing 1000 lines of code) and you want to use the best model for it.
        """
        logger.info(f"[Delegation] Spawning specialist sub-agent (Model: {target_model}) for task: {task[:50]}...")
        
        # Verify the router has the requested model
        if not hasattr(self.engine, 'llm') or target_model not in self.engine.llm.providers:
            return f"Error: Model '{target_model}' is not configured in LLMRouter. Available: {list(self.engine.llm.providers.keys()) if hasattr(self.engine, 'llm') else 'None'}"

        # Construct isolated context for the sub-agent
        messages = [
            LLMMessage(role=Role.SYSTEM, content=f"You are a F.R.I.D.A.Y. sub-agent. Your role is: {role_description}. Execute the following task accurately and completely."),
            LLMMessage(role=Role.USER, content=task)
        ]

        try:
            # Route to specific provider via LLMRouter
            response = await self.engine.llm.chat(
                messages=messages,
                preferred_provider=target_model,
                temperature=0.2
            )
            
            logger.info(f"[Delegation] Specialist agent (Model: {response.provider}) completed task.")
            
            return (
                f"--- SPECIALIST AGENT REPORT ({response.provider}) ---\n"
                f"{response.content}\n"
                f"---------------------------------------------------"
            )
        except Exception as e:
            logger.error(f"[Delegation] Specialist agent failed: {e}")
            return f"Error running specialist agent: {str(e)}"
