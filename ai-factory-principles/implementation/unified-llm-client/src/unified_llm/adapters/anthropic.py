"""
Anthropic adapter using the Messages API.

Uses the native Anthropic Messages API (/v1/messages) with support for:
- Extended thinking (thinking blocks)
- Prompt caching (cache_control)
- Beta feature headers
- Tool calling
- Streaming
"""

import json
import httpx
from typing import AsyncIterator, List, Dict, Any, Optional
from datetime import datetime

from ..adapter import ProviderAdapter, ProviderError, AuthenticationError, RateLimitError
from ..models import (
    Request, Response, StreamEvent, Message, ContentPart, ContentKind,
    Role, ToolCall, Usage, FinishReason, ToolCallData
)


class AnthropicAdapter(ProviderAdapter):
    """
    Anthropic provider adapter.

    Uses the Messages API with automatic prompt caching injection.
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://api.anthropic.com"
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers=self._default_headers()
        )

    @property
    def name(self) -> str:
        return "anthropic"

    def _default_headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2025-02-15",
            "content-type": "application/json"
        }

    async def complete(self, request: Request) -> Response:
        """Send a blocking request to Anthropic Messages API."""
        # Convert unified request to Anthropic format
        anthropic_request = self._build_request(request, stream=False)

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/messages",
                json=anthropic_request,
                headers=self._headers_for_request(request)
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)

        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """Stream a response from Anthropic Messages API."""
        anthropic_request = self._build_request(request, stream=True)

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/messages",
                json=anthropic_request,
                headers=self._headers_for_request(request)
            )
            response.raise_for_status()

            # Read stream line by line
            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                # Handle SSE format
                if line.startswith("event:"):
                    continue  # Skip event type lines
                if not line.startswith("data: "):
                    continue

                data_str = line[6:]  # Remove "data: " prefix
                if data_str == "[DONE]":
                    break

                try:
                    data = json.loads(data_str)
                    event = self._parse_stream_event(data)
                    if event:
                        yield event
                except json.JSONDecodeError:
                    # Skip malformed JSON
                    continue

        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    def _build_request(self, request: Request, stream: bool) -> Dict[str, Any]:
        """Convert unified Request to Anthropic Messages API format."""
        # Extract system messages
        system_parts = []
        regular_messages = []

        for msg in request.messages:
            if msg.role == Role.SYSTEM:
                system_parts.append(msg.text)
            else:
                regular_messages.append(msg)

        # Build Anthropic messages with cache_control injection
        messages = self._convert_messages_with_caching(regular_messages)

        # Build request body
        body = {
            "model": request.model,
            "messages": messages,
            "stream": stream
        }

        # Add system prompt if any
        if system_parts:
            # Add cache_control to system prompt for caching
            body["system"] = [
                {
                    "type": "text",
                    "text": "\n\n".join(system_parts),
                    "cache_control": {"type": "ephemeral"}
                }
            ]

        # Add optional parameters
        if request.max_tokens:
            body["max_tokens"] = request.max_tokens
        else:
            # Anthropic requires max_tokens
            body["max_tokens"] = 4096

        if request.temperature is not None:
            body["temperature"] = request.temperature

        if request.top_p is not None:
            body["top_p"] = request.top_p

        # Add tools if provided
        if request.tools:
            body["tools"] = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.parameters
                }
                for tool in request.tools
            ]

            # Map tool_choice
            if request.tool_choice:
                if request.tool_choice == "required":
                    body["tool_choice"] = {"type": "any"}
                elif request.tool_choice == "auto":
                    body["tool_choice"] = {"type": "auto"}
                elif request.tool_choice != "none":
                    # Specific tool name
                    body["tool_choice"] = {
                        "type": "tool",
                        "name": request.tool_choice
                    }

        return body

    def _convert_messages_with_caching(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """
        Convert messages to Anthropic format with intelligent cache_control injection.

        Anthropic prompt caching strategy:
        - Cache system prompt (done in _build_request)
        - Cache the conversation history up to the last 2 turns
        - This maximizes cache hits for agentic loops
        """
        anthropic_messages = []

        for i, msg in enumerate(messages):
            # Convert role
            if msg.role == Role.USER:
                role = "user"
            elif msg.role == Role.ASSISTANT:
                role = "assistant"
            elif msg.role == Role.TOOL:
                # Tool results get wrapped in user message
                role = "user"
            else:
                continue  # Skip system, developer (handled separately)

            # Convert content
            content = self._convert_content(msg)

            # Add cache_control to the last user message before the final turn
            # This caches the entire conversation history
            is_cacheable_message = (
                role == "user" and
                i < len(messages) - 2  # Not in the last 2 messages
            )

            if is_cacheable_message and isinstance(content, list):
                # Add cache breakpoint to the last content block
                if content:
                    content[-1]["cache_control"] = {"type": "ephemeral"}

            anthropic_messages.append({
                "role": role,
                "content": content
            })

        return anthropic_messages

    def _convert_content(self, msg: Message) -> Any:
        """Convert message content to Anthropic format."""
        if len(msg.content) == 1 and msg.content[0].kind == ContentKind.TEXT:
            # Simple text message
            return msg.content[0].text

        # Multimodal or complex content
        content_blocks = []
        for part in msg.content:
            if part.kind == ContentKind.TEXT:
                content_blocks.append({
                    "type": "text",
                    "text": part.text
                })
            elif part.kind == ContentKind.IMAGE:
                if part.image.url:
                    content_blocks.append({
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": part.image.url
                        }
                    })
                elif part.image.data:
                    import base64
                    content_blocks.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": part.image.media_type or "image/png",
                            "data": base64.b64encode(part.image.data).decode()
                        }
                    })
            elif part.kind == ContentKind.TOOL_RESULT:
                content_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": part.tool_result.tool_call_id,
                    "content": part.tool_result.content,
                    "is_error": part.tool_result.is_error
                })
            elif part.kind == ContentKind.TOOL_CALL:
                content_blocks.append({
                    "type": "tool_use",
                    "id": part.tool_call.id,
                    "name": part.tool_call.name,
                    "input": part.tool_call.arguments
                })

        return content_blocks

    def _parse_response(self, data: Dict[str, Any]) -> Response:
        """Parse Anthropic response to unified Response."""
        # Extract text
        text_parts = []
        tool_calls = []
        thinking = None

        for block in data.get("content", []):
            if block["type"] == "text":
                text_parts.append(block["text"])
            elif block["type"] == "thinking":
                thinking = block.get("thinking", "")
            elif block["type"] == "tool_use":
                tool_calls.append(ToolCall(
                    id=block["id"],
                    name=block["name"],
                    arguments=block["input"]
                ))

        # Map finish reason
        stop_reason = data.get("stop_reason")
        if stop_reason == "end_turn":
            finish_reason = FinishReason.STOP
        elif stop_reason == "max_tokens":
            finish_reason = FinishReason.LENGTH
        elif stop_reason == "tool_use":
            finish_reason = FinishReason.TOOL_CALLS
        else:
            finish_reason = FinishReason.STOP

        # Parse usage
        usage_data = data.get("usage", {})
        usage = Usage(
            input_tokens=usage_data.get("input_tokens", 0),
            output_tokens=usage_data.get("output_tokens", 0),
            total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
            cache_read_tokens=usage_data.get("cache_read_input_tokens", 0),
            cache_write_tokens=usage_data.get("cache_creation_input_tokens", 0)
        )

        return Response(
            text="".join(text_parts),
            finish_reason=finish_reason,
            usage=usage,
            tool_calls=tool_calls,
            reasoning=thinking,
            id=data.get("id"),
            model=data.get("model"),
            created=datetime.now()
        )

    def _parse_stream_event(self, data: Dict[str, Any]) -> Optional[StreamEvent]:
        """Parse a streaming event from Anthropic."""
        event_type = data.get("type")

        if event_type == "content_block_delta":
            delta = data.get("delta", {})
            if delta.get("type") == "text_delta":
                return StreamEvent(
                    kind="text_delta",
                    text=delta.get("text", "")
                )
            elif delta.get("type") == "thinking_delta":
                # Thinking content
                return StreamEvent(
                    kind="thinking_delta",
                    text=delta.get("thinking", "")
                )
        elif event_type == "message_delta":
            delta = data.get("delta", {})
            usage_data = data.get("usage", {})
            if usage_data:
                usage = Usage(
                    input_tokens=0,
                    output_tokens=usage_data.get("output_tokens", 0),
                    total_tokens=usage_data.get("output_tokens", 0)
                )
                return StreamEvent(
                    kind="usage_update",
                    usage=usage
                )

        return None

    def _headers_for_request(self, request: Request) -> Dict[str, str]:
        """Build headers including beta feature headers."""
        headers = self._default_headers()

        # Add beta headers if specified
        if request.provider_options and "anthropic" in request.provider_options:
            anthropic_opts = request.provider_options["anthropic"]
            beta_headers = anthropic_opts.get("beta_headers", [])
            if beta_headers:
                headers["anthropic-beta"] = ",".join(beta_headers)

        return headers

    def _handle_http_error(self, error: httpx.HTTPStatusError):
        """Convert HTTP errors to provider exceptions."""
        if error.response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error.response.text}")
        elif error.response.status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {error.response.text}")
        else:
            raise ProviderError(f"Anthropic API error: {error.response.text}")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
