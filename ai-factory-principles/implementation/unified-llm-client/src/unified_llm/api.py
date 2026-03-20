"""
High-level convenience API for the unified LLM client.

These functions provide the simplest interface for most use cases.
"""

from typing import List, Optional, Dict, Any, AsyncIterator
from .models import Message, Request, Response, StreamEvent, Tool
from .client import Client, get_default_client


async def generate(
    model: str,
    prompt: Optional[str] = None,
    messages: Optional[List[Message]] = None,
    system: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    reasoning_effort: Optional[str] = None,
    client: Optional[Client] = None,
    **kwargs
) -> Response:
    """
    Generate a response from an LLM.

    Simple interface for most use cases. Either provide:
    - `prompt` (simple string) OR
    - `messages` (full conversation)

    Args:
        model: Model identifier (e.g., "claude-opus-4-6", "gpt-5.2")
        prompt: Simple text prompt (creates a user message)
        messages: Full conversation history (mutually exclusive with prompt)
        system: System prompt to prepend
        tools: Tool definitions for function calling
        tool_choice: "auto", "required", "none", or tool name
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.0 to 2.0)
        reasoning_effort: "low", "medium", "high" (for reasoning models)
        client: Client to use (defaults to global client)
        **kwargs: Additional provider-specific options

    Returns:
        Response object with text, usage, tool calls, etc.

    Example:
        >>> response = await generate(
        ...     model="claude-opus-4-6",
        ...     prompt="What is 2+2?"
        ... )
        >>> print(response.text)
        "2+2 equals 4."
    """
    if client is None:
        client = get_default_client()

    # Build messages
    if messages is None:
        if prompt is None:
            raise ValueError("Must provide either 'prompt' or 'messages'")
        messages = [Message.user(prompt)]
    elif prompt is not None:
        raise ValueError("Cannot provide both 'prompt' and 'messages'")

    # Add system message if provided
    if system:
        messages = [Message.system(system)] + messages

    # Convert tools to Tool objects
    tool_objs = None
    if tools:
        tool_objs = [
            Tool(
                name=t["name"],
                description=t.get("description", ""),
                parameters=t.get("parameters", {})
            )
            for t in tools
        ]

    # Build request
    request = Request(
        model=model,
        messages=messages,
        tools=tool_objs,
        tool_choice=tool_choice,
        max_tokens=max_tokens,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        provider_options=kwargs.get("provider_options")
    )

    return await client.complete(request)


async def stream(
    model: str,
    prompt: Optional[str] = None,
    messages: Optional[List[Message]] = None,
    system: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    client: Optional[Client] = None,
    **kwargs
) -> AsyncIterator[StreamEvent]:
    """
    Stream a response from an LLM.

    Args:
        model: Model identifier
        prompt: Simple text prompt (creates a user message)
        messages: Full conversation history
        system: System prompt to prepend
        tools: Tool definitions
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        client: Client to use
        **kwargs: Additional options

    Yields:
        StreamEvent objects as they arrive

    Example:
        >>> async for chunk in stream(model="gpt-5.2", prompt="Count to 10"):
        ...     if chunk.text:
        ...         print(chunk.text, end="", flush=True)
    """
    if client is None:
        client = get_default_client()

    # Build messages
    if messages is None:
        if prompt is None:
            raise ValueError("Must provide either 'prompt' or 'messages'")
        messages = [Message.user(prompt)]
    elif prompt is not None:
        raise ValueError("Cannot provide both 'prompt' and 'messages'")

    # Add system message if provided
    if system:
        messages = [Message.system(system)] + messages

    # Convert tools
    tool_objs = None
    if tools:
        tool_objs = [
            Tool(
                name=t["name"],
                description=t.get("description", ""),
                parameters=t.get("parameters", {})
            )
            for t in tools
        ]

    # Build request
    request = Request(
        model=model,
        messages=messages,
        tools=tool_objs,
        max_tokens=max_tokens,
        temperature=temperature,
        provider_options=kwargs.get("provider_options")
    )

    async for event in client.stream(request):
        yield event
