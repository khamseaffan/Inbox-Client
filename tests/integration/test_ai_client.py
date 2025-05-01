from ai_conversation_client import AIConversationClient


def test_ai_response_format(monkeypatch):
    """Ensure AI client response contains a digit string for % spam."""

    class MockGemini:
        def send(self, _prompt: str) -> dict:
            return {"content": "87"}  # Simulated response

        def start_new_session(self, user_id: str) -> str:
            return "mock-session-id"

        def end_session(self, session_id: str) -> None:
            pass

    ai_client = AIConversationClient(MockGemini())
    session_id = ai_client.start_new_session("test_user")
    response = ai_client.send_message(session_id, "Is this spam?")
    content = response["content"]
    assert any(char.isdigit() for char in content)
    ai_client.end_session(session_id)
