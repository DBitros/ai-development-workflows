"""
OpenAI adapter using the Responses API.

TODO: Full implementation of OpenAI Responses API adapter.
For now, this is a placeholder that shows the structure.
"""

from typing import AsyncIterator, Optional
import httpx

from ..adapter import ProviderAdapter
from ..models import Request, Response, StreamEvent


class OpenAIAdapter(ProviderAdapter):
    """
    OpenAI provider adapter.

    Uses the Responses API (/v1/responses) for proper reasoning token support.
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        org_id: Optional[str] = None,
        timeout: float = 60.0
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com"
        self.org_id = org_id
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    @property
    def name(self) -> str:
        return "openai"

    async def complete(self, request: Request) -> Response:
        """Send a blocking request to OpenAI Responses API."""
        # TODO: Implement full OpenAI adapter
        # For now, raise not implemented
        raise NotImplementedError(
            "OpenAI adapter not yet implemented. "
            "This will use the Responses API (/v1/responses) for proper "
            "reasoning token support and built-in tools."
        )

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """Stream a response from OpenAI Responses API."""
        # TODO: Implement streaming
        raise NotImplementedError("OpenAI streaming not yet implemented")
        yield  # Make this a generator

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
