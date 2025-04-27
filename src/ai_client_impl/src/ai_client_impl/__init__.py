"""
AI Conversation Client package.

This module exposes the main AIConversationClient class.
"""

import ai_client

from ._impl import GeminiAPIClient

def get_client_impl() -> ai_client.IAIConversationClient:
    """Return an instance of the concrete GmailClient."""
    return GeminiAPIClient()

ai_client.get_client = get_client_impl
