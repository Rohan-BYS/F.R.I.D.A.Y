"""
Data models and schemas for dynamic tool generation in Tool Forge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ParameterType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"


class ToolParameter(BaseModel):
    name: str
    type: ParameterType = ParameterType.STRING
    description: str
    required: bool = True
    default: Optional[Any] = None


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter] = Field(default_factory=list)
    version: str = "1.0.0"
    author: str = "F.R.I.D.A.Y. Tool Forge"
    code: Optional[str] = None
    test_code: Optional[str] = None


@dataclass
class ToolExecutionResult:
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_seconds: float = 0.0
    stdout: str = ""
    stderr: str = ""
