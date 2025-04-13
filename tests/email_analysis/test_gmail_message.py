from tests.message.test_mock_message import MockGmailMessage

mock_message = {
    "id": "123abc",
    "payload": {
        "headers": [
            {"name": "From", "value": "test@example.com"},
            {"name": "Subject", "value": "Test Email"},
        ],
        "body": {
            "data": "VGhpcyBpcyBhIHRlc3QgZW1haWwu"  # base64 for "This is a test email."
        },
    }
}

def test_parse_from_field():
    msg = MockGmailMessage.from_api_dict(mock_message)
    assert msg.sender == "test@example.com"


def test_parse_subject_field():
    msg = MockGmailMessage.from_api_dict(mock_message)
    assert msg.subject == "Test Email"


def test_parse_body_content():
    msg = MockGmailMessage.from_api_dict(mock_message)
    assert "test email" in msg.body.lower()
