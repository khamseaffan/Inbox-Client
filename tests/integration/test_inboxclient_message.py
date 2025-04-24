import base64
import pytest
import message  # Import the message protocol package
import inbox_client_protocol # Import the client protocol package

# Ensure the implementation is imported so the factory override works
import message_impl
import inbox_client_impl

def test_get_message_factory() -> None:
    """Test that the message factory function can be called."""
    # Use dummy data for this basic check
    dummy_id = "test_id_123"
    # Need valid base64 data for a minimal email structure
    dummy_raw_data = base64.urlsafe_b64encode(b"Subject: Test\n\nBody").decode('utf-8')
    msg = message.get_message(msg_id=dummy_id, raw_data=dummy_raw_data)
    assert msg is not None
    assert msg.id == dummy_id

def test_get_client_factory() -> None:
    """Test that the client factory function can be called."""
    # This test will likely fail in CI without mocking or real credentials
    # For now, just check if it returns something without erroring immediately
    # (assuming the override works)
    try:
        # This might still fail if credentials.json is missing locally
        # and the test isn't properly mocked
        client = inbox_client_protocol.get_client()
        assert client is not None
    except FileNotFoundError:
        # If testing locally without credentials, this might be expected
        # In CI, this test should ideally be mocked or skipped
        pytest.skip("Skipping client factory test: credentials.json not found or test not mocked.")
    except Exception as e:
        pytest.fail(f"Client factory raised unexpected exception: {e}")

