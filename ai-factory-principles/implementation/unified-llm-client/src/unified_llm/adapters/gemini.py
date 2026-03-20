"""
Gemini adapter using the native Gemini API.

TODO: Full implementation of Gemini API adapter.
For now, this is a placeholder that shows the structure.
"""

from typing import AsyncIterator, Optional
import httpx

from ..adapter import ProviderAdapter
from ..models import Request, Response, StreamEvent


class GeminiAdapter(ProviderAdapter):
    """
    Gemini provider adapter.

    Uses the native Gemini API (/v1beta/models/*/generateContent) with
    support for grounding, code execution, and system instructions.
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 60.0
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://generativelanguage.googleapis.com"
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    @property
    def name(self) -> str:
        return "gemini"

    async def complete(self, request: Request) -> Response:
        """Send a blocking request to Gemini API."""
        # TODO: Implement full Gemini adapter
        raise NotImplementedError(
            "Gemini adapter not yet implemented. "
            "This will use the native Gemini API (/v1beta/models/*/generateContent) "
            "with support for grounding, code execution, and system instructions."
        )

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """Stream a response from Gemini API."""
        # TODO: Implement streaming
        raise NotImplementedError("Gemini streaming not yet implemented")
        yield  # Make this a generator

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
