from unittest.mock import Mock
from collections.abc import Iterator

import pytest

from src.inbox_client_api.src.inbox_client_api import Client
from src.message.src.message import Message

"Unit Tests for Client Protocol"

def test_get_messages() -> None:
    """Test get_messages method returns an iterator of Message objects."""
    client = Client.get_client()
    messages = client.get_messages()
    # Check that result is an iterator by verifying the presence of __iter__ and __next__
    assert hasattr(messages, '__iter__') and hasattr(messages, '__next__')
    # Verify that every element in the iterator is a Message instance
    assert all(isinstance(messages, Message) for msg in messages)

def test_send_message() -> None:
    """Test send_message method returns True for valid parameters."""
    client = Client.get_client()
    result = client.send_message("kc4433@gmail.com", "Subject", "Body")
    # Assert that send_message returns True as expected
    assert result is True

def test_delete_message() -> None:
    """Test delete_message method returns True when a valid message ID is provided."""
    client = Client.get_client()
    messages = client.get_messages()
    msg = next(messages)
    result = client.delete_message(msg.id)
    # Assert that delete_message returns True as expected
    assert result is True

def test_mark_as_read() -> None:
    """Test mark_as_read method returns True when a valid message ID is provided."""
    client = Client.get_client()
    messages = client.get_messages()
    msg = next(messages)    
    result = client.mark_as_read(msg.id)
    # Assert that mark_as_read returns True as expected
    assert result is True
