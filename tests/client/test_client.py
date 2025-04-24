from unittest.mock import Mock
from collections.abc import Iterator
import message
import inbox_client_protocol

import pytest

import inbox_client_impl
import message_impl
"Unit Tests for Client Protocol"

@pytest.fixture
def mock_client() -> Mock:
    """Provides a mocked Client instance."""
    client = Mock(spec=inbox_client_protocol.Client)

    mock_msg1 = Mock(spec=message.Message)
    mock_msg1.id = "mock_id_1"
    mock_msg2 = Mock(spec=message.Message)
    mock_msg2.id = "mock_id_2"
    client.get_messages.return_value = iter([mock_msg1, mock_msg2]) # Return an iterator

    client.send_message.return_value = True

    client.delete_message.return_value = True

    client.mark_as_read.return_value = True

    return client


def test_get_messages() -> None:
    """Test get_messages method returns an iterator of Message objects."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    # Check that result is an iterator by verifying the presence of __iter__ and __next__
    assert hasattr(messages, '__iter__') and hasattr(messages, '__next__')

    msg_list = list(messages)

    # Verify that every element in the iterator is a Message instance
    assert all(isinstance(msg, Mock) for msg in msg_list)
    assert all(isinstance(msg, message.Message) for msg in messages)

def test_send_message() -> None:
    """Test send_message method returns True for valid parameters."""
    client = inbox_client_protocol.get_client()
    result = client.send_message("kc4433@gmail.com", "Subject", "Body")
    # Assert that send_message returns True as expected
    assert result is True

def test_delete_message() -> None:
    """Test delete_message method returns True when a valid message ID is provided."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    msg = next(messages)
    result = client.delete_message(msg.id)
    # Assert that delete_message returns True as expected
    assert result is True

def test_mark_as_read() -> None:
    """Test mark_as_read method returns True when a valid message ID is provided."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    msg = next(messages)    
    result = client.mark_as_read(msg.id)
    # Assert that mark_as_read returns True as expected
    assert result is True
