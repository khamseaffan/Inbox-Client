from unittest.mock import MagicMock
from tests.client.test_mock_client import MockGmailClient

def test_fetch_emails_returns_messages():
    fake_service = MagicMock()
    fake_service.users().messages().list().execute.return_value = {
        "messages": [{"id": "1"}, {"id": "2"}]
    }

    client = MockGmailClient(service=fake_service)
    result = client.fetch_emails()

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"
