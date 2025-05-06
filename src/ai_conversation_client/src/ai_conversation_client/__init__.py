"""
AI Conversation Client package.

This module exposes the main AIConversationClient class and implements dependency injection
to provide the GeminiAPIClient as the default implementation.
"""

from typing import Any
from collections.abc import Callable

from .client import AIConversationClient
from .gemini_api_client import GeminiAPIClient
from .interface import IAIConversationClient

# Default implementation of the AI conversation client
_default_client = None

def get_client() -> AIConversationClient:
    """Return an instance of the AIConversationClient with default implementation."""
    global _default_client # noqa: PLW0603
    # This exception is necessary to make their implementation work with dependency injection, with minimal edits...
    if _default_client is None:
        _default_client = AIConversationClient(api_client=GeminiAPIClient())
    return _default_client

# Expose the public API
__all__ = ["AIConversationClient", "GeminiAPIClient", "IAIConversationClient", "get_client"]
