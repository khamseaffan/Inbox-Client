import inbox_client_protocol
import inbox_client_impl
from unittest.mock import patch, MagicMock, ANY
from inbox_client_impl._impl import GmailClient
from collections.abc import Iterator
from google.auth.credentials import Credentials
import pytest

@pytest.fixture
def mock_google_service() -> MagicMock:
    """Provide mock Google API service resource object."""
    mock_service = MagicMock(name="Google Service Resource")
    # Mock the chained calls structure used in the methods
    mock_users = mock_service.users.return_value
    mock_messages = mock_users.messages.return_value
    # Configure default return values for execute() on different calls
    mock_messages.list.return_value.execute.return_value = {"messages": []} # Default: no messages #noqa: E501
    mock_messages.get.return_value.execute.return_value = {"raw": ""} # Default: empty raw data #noqa: E501
    mock_messages.send.return_value.execute.return_value = {"id": "sent_id_123"} # Default: success #noqa: E501
    mock_messages.delete.return_value.execute.return_value = {} # Default: success (no return needed) #noqa: E501
    mock_messages.modify.return_value.execute.return_value = {} # Default: success
    return mock_service

@pytest.fixture
def gmail_client(mock_google_service: MagicMock) -> GmailClient:
    """Provide GmailClient instance initialized with a mocked service."""
    # Instantiate the client directly, bypassing the complex __init__ auth logic
    return GmailClient(service=mock_google_service)


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

@patch("inbox_client_impl._impl.build")
@patch("inbox_client_impl._impl.Request")
@patch("inbox_client_impl._impl.Credentials")
@patch("os.environ.get")
def test_init_with_env_vars(mock_getenv, mock_creds_class, mock_request, mock_build) -> None: #type: ignore[no-untyped-def] # noqa: ANN001, ARG001
    """Test __init__ authentication using environment variables."""
    # Configure mocks
    mock_getenv.side_effect = lambda key, default=None: {
        "GMAIL_CLIENT_ID": "env_client_id",
        "GMAIL_CLIENT_SECRET": "env_client_secret",
        "GMAIL_REFRESH_TOKEN": "env_refresh_token",
        "GMAIL_TOKEN_URI": "env_token_uri"
    }.get(key, default)
    mock_creds_instance = mock_creds_class.return_value
    mock_build.return_value = MagicMock(name="Mock Service from Build")

    # Instantiate - this should trigger the env var logic
    client = GmailClient(service=None)

    # Assertions
    mock_creds_class.assert_called_once_with(
        None,
        refresh_token="env_refresh_token", # noqa: S106
        token_uri="env_token_uri", # noqa: S106
        client_id="env_client_id",
        client_secret="env_client_secret", # noqa: S106
        scopes=GmailClient.SCOPES
    )
    mock_creds_instance.refresh.assert_called_once()
    mock_build.assert_called_once_with("gmail", "v1", credentials=mock_creds_instance)
    assert client.service == mock_build.return_value

def test_get_messages_get_error(gmail_client: GmailClient, mock_google_service: MagicMock, capsys) -> None: # type: ignore[no-untyped-def] # noqa: E501, ANN001, ARG001
    """Test get_messages handles API errors during get."""
    list_response = {"messages": [{"id": "msg1"}]}
    mock_google_service.users.return_value.messages.return_value.list.return_value.execute.return_value = list_response # noqa: E501
    # Simulate error on the 'get' call
    mock_google_service.users.return_value.messages.return_value.get.return_value.execute.side_effect = Exception("Get API Failed") # noqa: E501

    # Consume the iterator - it should likely yield nothing or raise
    messages_iter = gmail_client.get_messages()
    # Depending on desired error handling, assert it raises or yields nothing
    with pytest.raises(Exception, match="Get API Failed"):
        list(messages_iter)

    # Verify list was called, but get might have been called once before error
    mock_google_service.users.return_value.messages.return_value.list.assert_called_once()
    mock_google_service.users.return_value.messages.return_value.get.assert_called_once_with(userId="me", id="msg1", format="raw") # noqa: E501

@patch("inbox_client_impl._impl.build")
@patch("inbox_client_impl._impl.Request")
@patch("inbox_client_impl._impl.Credentials")
@patch("os.path.exists")
def test_init_refresh_from_file(mock_exists, mock_creds_class, mock_request, mock_build, monkeypatch) -> None: #type: ignore[no-untyped-def] # noqa: E501, ANN001, ARG001
    """Test __init__ refreshing an expired token from file."""
    # Simulate token.json exists, credentials.json doesn't matter yet
    mock_exists.side_effect = lambda path: path == "token.json"

    # Simulate loaded credentials that are expired but have refresh token
    mock_expired_creds = MagicMock(spec=Credentials)
    mock_expired_creds.valid = False
    mock_expired_creds.expired = True
    mock_expired_creds.refresh_token = "file_refresh_token" # noqa: S105
    # Make from_authorized_user_file return this mock
    mock_creds_class.from_authorized_user_file.return_value = mock_expired_creds

    # Mock the build service
    mock_build.return_value = MagicMock(name="Mock Service from Build")

    # Instantiate - should trigger refresh logic
    client = GmailClient(service=None)

    # Assertions
    mock_creds_class.from_authorized_user_file.assert_called_once_with("token.json", GmailClient.SCOPES) # noqa: E501
    mock_expired_creds.refresh.assert_called_once() # Check refresh was called
    mock_build.assert_called_once_with("gmail", "v1", credentials=mock_expired_creds)
    assert client.service == mock_build.return_value

def test_get_messages_api_error(gmail_client: GmailClient, mock_google_service: MagicMock, capsys) -> None: # type: ignore[no-untyped-def] # noqa: E501, ANN001, ARG001
    """Test get_messages handles API errors during list gracefully."""
    mock_google_service.users.return_value.messages.return_value.list.return_value.execute.side_effect = Exception("List API Failed") # noqa: E501

    # Consume the iterator within a try-except or check if it's empty
    messages_iter = gmail_client.get_messages()
    with pytest.raises(Exception, match="List API Failed"):
         list(messages_iter) # Attempt to consume
