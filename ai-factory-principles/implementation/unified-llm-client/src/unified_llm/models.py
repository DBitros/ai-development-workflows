"""
Core data models for the Unified LLM Client.

These types provide a provider-agnostic representation of LLM conversations,
requests, and responses.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


class Role(str, Enum):
    """Message roles across all providers."""
    SYSTEM = "system"        # High-level instructions
    USER = "user"            # Human input
    ASSISTANT = "assistant"  # Model output
    TOOL = "tool"            # Tool execution results
    DEVELOPER = "developer"  # Privileged app instructions


class ContentKind(str, Enum):
    """Types of content parts in messages."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    THINKING = "thinking"
    REDACTED_THINKING = "redacted_thinking"


@dataclass
class ImageData:
    """Image content (URL or base64 data)."""
    url: Optional[str] = None
    data: Optional[bytes] = None
    media_type: Optional[str] = None  # "image/png", "image/jpeg"
    detail: Optional[str] = None      # "auto", "low", "high" (OpenAI)


@dataclass
class AudioData:
    """Audio content."""
    url: Optional[str] = None
    data: Optional[bytes] = None
    media_type: Optional[str] = None  # "audio/wav", "audio/mp3"


@dataclass
class DocumentData:
    """Document content (PDF, etc.)."""
    url: Optional[str] = None
    data: Optional[bytes] = None
    media_type: Optional[str] = None  # "application/pdf"


@dataclass
class ToolCallData:
    """Model-initiated tool invocation."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResultData:
    """Result of tool execution."""
    tool_call_id: str
    content: str
    is_error: bool = False


@dataclass
class ThinkingData:
    """Reasoning/thinking content."""
    content: str
    signature: Optional[str] = None  # For Anthropic's redacted thinking


@dataclass
class ContentPart:
    """
    A single part of message content (text, image, tool call, etc.).
    Uses tagged-union pattern: `kind` determines which data field is populated.
    """
    kind: Union[ContentKind, str]
    text: Optional[str] = None
    image: Optional[ImageData] = None
    audio: Optional[AudioData] = None
    document: Optional[DocumentData] = None
    tool_call: Optional[ToolCallData] = None
    tool_result: Optional[ToolResultData] = None
    thinking: Optional[ThinkingData] = None

    @staticmethod
    def text_part(text: str) -> "ContentPart":
        """Create a text content part."""
        return ContentPart(kind=ContentKind.TEXT, text=text)

    @staticmethod
    def image_part(url: Optional[str] = None, data: Optional[bytes] = None,
                   media_type: Optional[str] = None) -> "ContentPart":
        """Create an image content part."""
        return ContentPart(
            kind=ContentKind.IMAGE,
            image=ImageData(url=url, data=data, media_type=media_type)
        )

    @staticmethod
    def tool_call_part(id: str, name: str, arguments: Dict[str, Any]) -> "ContentPart":
        """Create a tool call content part."""
        return ContentPart(
            kind=ContentKind.TOOL_CALL,
            tool_call=ToolCallData(id=id, name=name, arguments=arguments)
        )

    @staticmethod
    def tool_result_part(tool_call_id: str, content: str, is_error: bool = False) -> "ContentPart":
        """Create a tool result content part."""
        return ContentPart(
            kind=ContentKind.TOOL_RESULT,
            tool_result=ToolResultData(tool_call_id=tool_call_id, content=content, is_error=is_error)
        )


@dataclass
class Message:
    """A single message in a conversation."""
    role: Role
    content: List[ContentPart]
    name: Optional[str] = None          # For tool messages, developer attribution
    tool_call_id: Optional[str] = None  # Links tool result to its call

    @property
    def text(self) -> str:
        """Concatenate all text content parts."""
        texts = [part.text for part in self.content if part.kind == ContentKind.TEXT and part.text]
        return "".join(texts)

    @staticmethod
    def system(content: str) -> "Message":
        """Create a system message."""
        return Message(
            role=Role.SYSTEM,
            content=[ContentPart.text_part(content)]
        )

    @staticmethod
    def user(content: str) -> "Message":
        """Create a user message."""
        return Message(
            role=Role.USER,
            content=[ContentPart.text_part(content)]
        )

    @staticmethod
    def assistant(content: str) -> "Message":
        """Create an assistant message."""
        return Message(
            role=Role.ASSISTANT,
            content=[ContentPart.text_part(content)]
        )

    @staticmethod
    def tool_result(tool_call_id: str, content: str, is_error: bool = False) -> "Message":
        """Create a tool result message."""
        return Message(
            role=Role.TOOL,
            content=[ContentPart.tool_result_part(tool_call_id, content, is_error)],
            tool_call_id=tool_call_id
        )


@dataclass
class Tool:
    """Tool definition for function calling."""
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema


@dataclass
class ToolCall:
    """A tool invocation requested by the model."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    """Result of executing a tool call."""
    tool_call_id: str
    content: str
    is_error: bool = False


@dataclass
class Usage:
    """Token usage statistics."""
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cache_read_tokens: int = 0   # Cached input tokens (OpenAI, Anthropic, Gemini)
    cache_write_tokens: int = 0  # Tokens written to cache
    reasoning_tokens: int = 0    # Reasoning/thinking tokens (OpenAI, Anthropic)


class FinishReason(str, Enum):
    """Why the model stopped generating."""
    STOP = "stop"                  # Natural completion
    LENGTH = "length"              # Hit max tokens
    TOOL_CALLS = "tool_calls"      # Made tool calls
    CONTENT_FILTER = "content_filter"  # Blocked by safety filter
    ERROR = "error"                # Error occurred


@dataclass
class Request:
    """Request to an LLM provider."""
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[str] = None  # "auto", "required", "none", or specific tool name
    reasoning_effort: Optional[str] = None  # "low", "medium", "high" (for reasoning models)
    provider: Optional[str] = None  # Explicit provider override
    provider_options: Optional[Dict[str, Any]] = None  # Provider-specific options


@dataclass
class Response:
    """Response from an LLM provider."""
    text: str
    finish_reason: FinishReason
    usage: Usage
    tool_calls: List[ToolCall] = field(default_factory=list)
    reasoning: Optional[str] = None  # Thinking/reasoning content
    id: Optional[str] = None         # Provider response ID
    model: Optional[str] = None      # Actual model used
    created: Optional[datetime] = None


@dataclass
class StreamEvent:
    """Event in a streaming response."""
    kind: str  # "text_delta", "tool_call_start", "tool_call_delta", "done"
    text: Optional[str] = None
    tool_call: Optional[ToolCall] = None
    tool_call_delta: Optional[Dict[str, Any]] = None
    usage: Optional[Usage] = None
    finish_reason: Optional[FinishReason] = None
