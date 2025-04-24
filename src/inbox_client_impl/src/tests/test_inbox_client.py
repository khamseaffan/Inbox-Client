import inbox_client_protocol
import inbox_client_impl
from unittest.mock import patch, MagicMock

# We need to patch 'GmailClient' where it's looked up by the code under test.
# The factory get_client_impl is in inbox_client_impl.__init__ and calls GmailClient()
# after importing it from ._impl. Let's patch the name 'GmailClient' as it exists
# within the 'inbox_client_impl' (specifically its __init__) module's namespace.
@patch("inbox_client_impl.GmailClient")
def test_inbox_client_creation(mock_gmail_client_class: MagicMock) -> None:
    """Test the creation of an inbox client using the factory function."""
    mock_instance = mock_gmail_client_class.return_value
    mock_instance.some_method.return_value = "mocked result"

    # Call the factory function. This will now call the mocked GmailClient()
    client = inbox_client_protocol.get_client()

    # Assert that the factory returned *something* (our mock instance)
    assert client is not None

    # Verify that the GmailClient class was indeed instantiated (called) once
    mock_gmail_client_class.assert_called_once()

    # Optional: Assert that the returned client is the instance created by the mock
    assert client == mock_gmail_client_class.return_value
