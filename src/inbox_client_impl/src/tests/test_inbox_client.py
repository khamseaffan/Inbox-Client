import inbox_client_protocol
import inbox_client_impl

def test_inbox_client_creation():
    """Test the creation of an inbox client."""
    client = inbox_client_protocol.get_client()
    assert client is not None