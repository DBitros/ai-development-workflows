"""
Unified LLM Client - Single interface across multiple LLM providers.

Based on StrongDM's unified-llm-spec.md from https://github.com/strongdm/attractor
"""

from .models import (
    Message,
    ContentPart,
    Role,
    ContentKind,
    Request,
    Response,
    Tool,
    ToolCall,
    ToolResult,
    Usage,
    StreamEvent,
)
from .client import Client
from .api import generate, stream

__version__ = "0.1.0"

__all__ = [
    # Core models
    "Message",
    "ContentPart",
    "Role",
    "ContentKind",
    "Request",
    "Response",
    "Tool",
    "ToolCall",
    "ToolResult",
    "Usage",
    "StreamEvent",
    # Client
    "Client",
    # High-level API
    "generate",
    "stream",
]
