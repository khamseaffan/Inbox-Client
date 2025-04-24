from unittest.mock import MagicMock

import pytest

import inbox_client_protocol
import inbox_client_impl
import message
import message_impl

@pytest.fixture
def initialize_a_message():
    """Fixture to create a mock message."""
    message_instance = message.get_message()
    return message_instance

@pytest.fixture
def initialize_an_inbox_client():
    """Fixture to create a mock inbox client."""
    inbox_client_instance = inbox_client_protocol.get_client()
    return inbox_client_instance