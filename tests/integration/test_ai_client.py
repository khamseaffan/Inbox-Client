from ai_conversation_client import AIConversationClient


def test_ai_response_format(monkeypatch):
    """Ensure AI client response contains a digit string for % spam."""

    class MockGemini:
        def send(self, prompt: str) -> dict:
            return {"content": "87"}  # Simulated response

    ai_client = AIConversationClient(MockGemini())
    session_id = ai_client.start_new_session("test_user")
    response = ai_client.send_message(session_id, "Is this spam?")
    content = response["content"]
    assert any(char.isdigit() for char in content)
    ai_client.end_session(session_id)
