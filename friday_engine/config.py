"""
F.R.I.D.A.Y. Configuration Engine
Strongly typed, validated configuration using Pydantic and PyYAML.
Supports YAML loading, environment variable overrides, and dynamic updating.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field


class SystemConfig(BaseModel):
    name: str = "F.R.I.D.A.Y."
    version: str = "1.0.0"
    creator: str = "Rohan"
    environment: str = "development"
    log_level: str = "INFO"
    data_dir: str = "data"


class GeminiConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    model: str = "gemini-2.0-flash"
    timeout: int = 30
    temperature: float = 0.2


class ClaudeConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    model: str = "claude-3-5-sonnet-20241022"
    timeout: int = 30
    temperature: float = 0.2


class OpenAIConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = "gpt-4o"
    base_url: str = "https://api.openai.com/v1"
    timeout: int = 30
    temperature: float = 0.2


class LocalLLMConfig(BaseModel):
    base_url: str = "http://127.0.0.1:8000/v1"
    model: str = "llama-3-8b-instruct"
    timeout: int = 60
    temperature: float = 0.2


class LLMConfig(BaseModel):
    priority: List[str] = Field(default_factory=lambda: ["gemini", "claude", "openai", "local"])
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    local: LocalLLMConfig = Field(default_factory=LocalLLMConfig)


class AgenticaConfig(BaseModel):
    mode: str = "http"  # 'http' or 'stdio'
    endpoint: str = "http://127.0.0.1:8000"
    timeout: int = 30
    headless: bool = False


class ToolForgeConfig(BaseModel):
    enabled: bool = True
    sandbox_dir: str = "data/forge_sandbox"
    generated_tools_dir: str = "friday_engine/tool_forge/custom_tools"
    test_timeout_seconds: int = 15
    auto_register: bool = True


class SubAgentsConfig(BaseModel):
    max_concurrent_workers: int = 4
    default_worker_timeout: int = 300
    enable_multiprocessing: bool = True


class SecurityConfig(BaseModel):
    vault_file: str = "data/identity_vault.enc"
    key_file: str = "data/identity_vault.key"
    auto_generate_key: bool = True


class MemoryConfig(BaseModel):
    db_path: str = "data/friday_state.db"
    busy_timeout_ms: int = 5000
    skills_dir: str = "data/skills"


class MidnightProtocolConfig(BaseModel):
    enabled: bool = True
    schedule_time: str = "00:00"
    git_remote: str = "origin"
    git_branch: str = "main"
    auto_push: bool = True
    commit_message_prefix: str = "Nightly auto-backup [Midnight Protocol]"


class FridayConfig(BaseModel):
    system: SystemConfig = Field(default_factory=SystemConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    agentica: AgenticaConfig = Field(default_factory=AgenticaConfig)
    tool_forge: ToolForgeConfig = Field(default_factory=ToolForgeConfig)
    sub_agents: SubAgentsConfig = Field(default_factory=SubAgentsConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    midnight_protocol: MidnightProtocolConfig = Field(default_factory=MidnightProtocolConfig)


def load_config(config_path: Optional[str | Path] = None) -> FridayConfig:
    """
    Load configuration from YAML file and environment variables.
    Falls back to sensible defaults if file does not exist.
    """
    if config_path is None:
        # Search relative to project root or module
        default_paths = [
            Path.cwd() / "friday_engine" / "config.yaml",
            Path.cwd() / "config.yaml",
            Path(__file__).parent / "config.yaml",
        ]
        for p in default_paths:
            if p.is_file():
                config_path = p
                break

    raw_data: dict = {}
    if config_path and Path(config_path).is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    raw_data = loaded
        except Exception as exc:
            print(f"[WARN] Failed to load config from {config_path}: {exc}. Using defaults.")

    config = FridayConfig.model_validate(raw_data)
    return config
