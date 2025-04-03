from unittest.mock import Mock
from collections.abc import Iterator

import pytest

from src.inbox_client_api.src.inbox_client_api import Client
from src.message.src.message import Message

"Unit Tests for Client Protocol"


def test_get_messages() -> None:
    """Test get_messages method."""
    client = Mock(spec=Client)
    msg_mock = Mock(spec=Message)
    client.get_messages.return_value = iter([msg_mock])
    result = client.get_messages() 
    assert hasattr(result, '__iter__') and hasattr(result, '__next__')
    msgs = list(result)
    assert all(isinstance(msg, Message) for msg in msgs)
