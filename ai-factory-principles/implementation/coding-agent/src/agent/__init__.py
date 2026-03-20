"""
Coding Agent - Autonomous coding agent with tool execution.

Based on StrongDM's coding-agent-loop-spec.md
"""

from .session import Session, SessionConfig, SessionState, SessionEvent, EventKind
from .tools import ToolRegistry, create_standard_tools

__version__ = "0.1.0"

__all__ = [
    "Session",
    "SessionConfig",
    "SessionState",
    "SessionEvent",
    "EventKind",
    "ToolRegistry",
    "create_standard_tools",
]
