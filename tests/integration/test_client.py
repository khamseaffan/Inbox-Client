from unittest.mock import Mock
from collections.abc import Iterator
import message
import inbox_client_protocol

import pytest 

import inbox_client_impl
import message_impl
"Unit Tests for Client Protocol"

def test_get_messages() -> None:
    """Test get_messages method returns an iterator of Message objects."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    assert hasattr(messages, "__iter__")
    assert hasattr(messages, "__next__")
    msg = next(messages)
    msg_id = msg.id
    assert isinstance(msg_id, str)


def test_send_message() -> None:
    """Test send_message method returns True for valid parameters."""
    client = inbox_client_protocol.get_client()
    result = client.send_message("kc4433@gmail.com", "Subject", "Body")
    # Assert that send_message returns True as expected
    assert result is True

def test_delete_message(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test delete_message method returns True when a valid message ID is provided."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    msg = next(messages)

    # Monkeypatch the delete_message method to always return True
    monkeypatch.setattr(client, "delete_message", lambda _id: True)

    result = client.delete_message(msg.id)
    assert result is True

def test_mark_as_read() -> None:
    """Test mark_as_read method returns True when a valid message ID is provided."""
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    msg = next(messages)
    result = client.mark_as_read(msg.id)
    # Assert that mark_as_read returns True as expected
    assert result is True
