"""
F.R.I.D.A.Y. (Fully Recursive Intelligent Digital Autonomous Yield)
Parent Forge Engine.
"""

__version__ = "1.2.0"
__author__ = "Rohan"

from friday_engine.aci.code_surgeon import CodeSurgeon, SurgeryResult
from friday_engine.aci.terminal import CommandObservation, VerifiedTerminal
from friday_engine.agentica.client import AgenticaClient
from friday_engine.backup.midnight import MidnightProtocol
from friday_engine.config import FridayConfig, load_config
from friday_engine.core.engine import FridayEngine
from friday_engine.evolution.distiller import SkillDistiller
from friday_engine.evolution.skill_store import SkillStore
from friday_engine.llm.router import LLMRouter
from friday_engine.logger import logger, setup_logger
from friday_engine.memory.memory_engine import PersistentMemoryEngine
from friday_engine.security.vault import IdentityVault
from friday_engine.self_heal.auto_patcher import AutoPatcher, PatchResult
from friday_engine.self_heal.diagnostic import SelfHealingDiagnostic
from friday_engine.sub_agents.pool import SubAgentPool
from friday_engine.tool_forge.forge import ToolForge

__all__ = [
    "FridayEngine",
    "FridayConfig",
    "load_config",
    "PersistentMemoryEngine",
    "SkillStore",
    "SkillDistiller",
    "CodeSurgeon",
    "SurgeryResult",
    "VerifiedTerminal",
    "CommandObservation",
    "AutoPatcher",
    "PatchResult",
    "SelfHealingDiagnostic",
    "LLMRouter",
    "ToolForge",
    "AgenticaClient",
    "SubAgentPool",
    "IdentityVault",
    "MidnightProtocol",
    "logger",
    "setup_logger",
    "__version__",
    "__author__",
]
