from unittest.mock import Mock
from collections.abc import Iterator

import pytest

from inbox_client_api import Client
from message import Message

"Unit Tests for Client Protocol"


def test_get_messages() -> None:
    """Test get_messages method returns an iterator of Message objects."""
    client = Mock(spec=Client)
    msg_mock = Mock(spec=Message)
    # Simulate get_messages returning an iterator with one dummy message
    client.get_messages.return_value = iter([msg_mock])
    result = client.get_messages()
    # Check that result is an iterator by
    # verifying the presence of __iter__ and __next__
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")
    msgs = list(result)
    # Verify that every element in the iterator is a Message instance
    assert all(isinstance(msg, Message) for msg in msgs)


def test_send_message() -> None:
    """Test send_message method returns True for valid parameters."""
    client = Mock(spec=Client)
    # Set a dummy return value for send_message
    client.send_message.return_value = True
    result = client.send_message("recipient@example.com", "Subject", "Body")
    # Assert that send_message returns True as expected
    assert result is True


def test_delete_message() -> None:
    """Test delete_message method returns True when a valid message ID is provided."""
    client = Mock(spec=Client)
    # Set a dummy return value for delete_message
    client.delete_message.return_value = True
    result = client.delete_message("123")
    # Assert that delete_message returns True as expected
    assert result is True


def test_mark_as_read() -> None:
    """Test mark_as_read method returns True when a valid message ID is provided."""
    client = Mock(spec=Client)
    # Set a dummy return value for mark_as_read
    client.mark_as_read.return_value = True
    result = client.mark_as_read("123")
    # Assert that mark_as_read returns True as expected
    assert result is True
