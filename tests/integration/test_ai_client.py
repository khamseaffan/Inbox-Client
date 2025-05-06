from typing import Any

import pytest
from ai_conversation_client import AIConversationClient # type: ignore[import-untyped]
from unittest.mock import patch, MagicMock
import os

# Patch environment variables for tests that need them
@pytest.mark.integration
def mock_env_vars():
    """Provide environment variables for testing."""
    with patch.dict(os.environ, {
        "GMAIL_CLIENT_ID": "test-client-id",
        "GMAIL_CLIENT_SECRET": "test-client-secret",
        "GMAIL_REFRESH_TOKEN": "test-refresh-token",
        "GMAIL_TOKEN_URI": "https://oauth2.googleapis.com/token",
        "GEMINI_API_KEY": "test-gemini-api-key"
    }):
        yield

@pytest.mark.integration
def test_ai_response_format() -> None:
    """Ensure AI client response contains a digit string for % spam."""

    class MockGemini:
        def send_message(self, _session_id: str, _message: str) -> dict[str, Any]:
            return {"content": "87"}

        def start_new_session(self, _user_id: str) -> str:
            return "mock-session-id"

        def end_session(self, _session_id: str) -> None:
            pass

    ai_client = AIConversationClient(MockGemini())
    session_id = ai_client.start_new_session("test_user")
    response = ai_client.send_message(session_id, "Is this spam?")
    content = response["content"]
    assert any(char.isdigit() for char in content)
    ai_client.end_session(session_id)
