"""
Main Client class for routing requests to providers.
"""

import os
from typing import Dict, Optional, List, Callable, AsyncIterator
from .models import Request, Response, StreamEvent
from .adapter import ProviderAdapter, ProviderError


class Client:
    """
    Orchestrates requests across multiple LLM providers.

    The Client:
    - Routes requests by provider identifier
    - Applies middleware (logging, caching, etc.)
    - Manages provider adapters
    """

    def __init__(
        self,
        providers: Dict[str, ProviderAdapter],
        default_provider: Optional[str] = None,
        middleware: Optional[List[Callable]] = None
    ):
        """
        Create a new client.

        Args:
            providers: Map of provider name -> adapter
            default_provider: Provider to use when not specified
            middleware: List of middleware functions
        """
        self.providers = providers
        self.default_provider = default_provider or self._infer_default()
        self.middleware = middleware or []

        # Note: Initialize will be called by host if needed
        # Not calling here to avoid async issues in constructor

    @classmethod
    def from_env(
        cls,
        middleware: Optional[List[Callable]] = None
    ) -> "Client":
        """
        Create a client from environment variables.

        Looks for:
        - OPENAI_API_KEY -> OpenAI adapter
        - ANTHROPIC_API_KEY -> Anthropic adapter
        - GEMINI_API_KEY -> Gemini adapter

        Args:
            middleware: Optional middleware functions

        Returns:
            Configured client

        Raises:
            ValueError: If no API keys found
        """
        from .adapters.openai import OpenAIAdapter
        from .adapters.anthropic import AnthropicAdapter
        from .adapters.gemini import GeminiAdapter

        providers = {}

        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            providers["openai"] = OpenAIAdapter(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
                org_id=os.getenv("OPENAI_ORG_ID")
            )

        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            providers["anthropic"] = AnthropicAdapter(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                base_url=os.getenv("ANTHROPIC_BASE_URL")
            )

        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            providers["gemini"] = GeminiAdapter(
                api_key=gemini_key,
                base_url=os.getenv("GEMINI_BASE_URL")
            )

        if not providers:
            raise ValueError(
                "No API keys found in environment. "
                "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY"
            )

        return cls(providers=providers, middleware=middleware)

    def _infer_default(self) -> Optional[str]:
        """Infer default provider (first registered)."""
        if not self.providers:
            return None
        return list(self.providers.keys())[0]

    def _resolve_provider(self, request: Request) -> str:
        """Determine which provider to use for this request."""
        if request.provider:
            if request.provider not in self.providers:
                raise ProviderError(
                    f"Provider '{request.provider}' not registered. "
                    f"Available: {list(self.providers.keys())}"
                )
            return request.provider

        if not self.default_provider:
            raise ProviderError(
                "No provider specified and no default configured"
            )

        return self.default_provider

    async def complete(self, request: Request) -> Response:
        """
        Send a request and block until complete.

        Args:
            request: Request to send

        Returns:
            Complete response

        Raises:
            ProviderError: On provider errors
        """
        provider_name = self._resolve_provider(request)
        adapter = self.providers[provider_name]

        # Apply middleware
        if self.middleware:
            return await self._apply_middleware(request, adapter.complete)

        return await adapter.complete(request)

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """
        Send a request and stream the response.

        Args:
            request: Request to send

        Yields:
            Stream events as they arrive

        Raises:
            ProviderError: On provider errors
        """
        provider_name = self._resolve_provider(request)
        adapter = self.providers[provider_name]

        # Apply middleware (streaming version)
        if self.middleware:
            async for event in self._apply_streaming_middleware(request, adapter.stream):
                yield event
        else:
            async for event in adapter.stream(request):
                yield event

    async def _apply_middleware(
        self,
        request: Request,
        handler: Callable
    ) -> Response:
        """Apply middleware chain to a blocking request."""
        async def next_handler(req):
            return await handler(req)

        # Build middleware chain (reverse order)
        for middleware in reversed(self.middleware):
            current_handler = next_handler
            async def next_handler(req, handler=current_handler, mw=middleware):
                return await mw(req, handler)

        return await next_handler(request)

    async def _apply_streaming_middleware(
        self,
        request: Request,
        handler: Callable
    ) -> AsyncIterator[StreamEvent]:
        """Apply middleware chain to a streaming request."""
        # For now, just pass through
        # TODO: Implement streaming middleware support
        async for event in handler(request):
            yield event

    async def close(self):
        """Close all provider adapters."""
        for adapter in self.providers.values():
            if hasattr(adapter, 'close'):
                await adapter.close()


# Global default client (lazy-initialized)
_default_client: Optional[Client] = None


def get_default_client() -> Client:
    """Get or create the global default client."""
    global _default_client
    if _default_client is None:
        _default_client = Client.from_env()
    return _default_client


def set_default_client(client: Client):
    """Set the global default client."""
    global _default_client
    _default_client = client
