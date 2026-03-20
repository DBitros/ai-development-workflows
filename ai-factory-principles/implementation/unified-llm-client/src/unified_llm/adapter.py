"""
Provider adapter interface.

All LLM providers must implement this interface to work with the unified client.
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator
from .models import Request, Response, StreamEvent


class ProviderAdapter(ABC):
    """
    Interface that every provider adapter must implement.

    Each provider speaks a different API (OpenAI Responses, Anthropic Messages,
    Gemini API). The adapter translates between the unified models and the
    provider's native format.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (e.g., "openai", "anthropic", "gemini")."""
        pass

    @abstractmethod
    async def complete(self, request: Request) -> Response:
        """
        Send a request, block until complete, return the full response.

        Args:
            request: Unified request object

        Returns:
            Unified response object

        Raises:
            ProviderError: On API errors
            AuthenticationError: On auth failures
            RateLimitError: On rate limit exceeded
        """
        pass

    @abstractmethod
    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """
        Send a request, return an async iterator of stream events.

        Args:
            request: Unified request object

        Yields:
            StreamEvent objects as they arrive

        Raises:
            ProviderError: On API errors
            AuthenticationError: On auth failures
            RateLimitError: On rate limit exceeded
        """
        pass

    async def close(self):
        """
        Release resources (HTTP connections, etc.).
        Optional to implement.
        """
        pass

    async def initialize(self):
        """
        Validate configuration on startup.
        Optional to implement.
        """
        pass

    def supports_tool_choice(self, mode: str) -> bool:
        """
        Check if a particular tool choice mode is supported.
        Optional to implement.
        """
        return mode in ["auto", "required", "none"]


class ProviderError(Exception):
    """Base exception for provider errors."""
    pass


class AuthenticationError(ProviderError):
    """Authentication failed."""
    pass


class RateLimitError(ProviderError):
    """Rate limit exceeded."""
    pass


class ContextLengthError(ProviderError):
    """Request exceeds context window."""
    pass
