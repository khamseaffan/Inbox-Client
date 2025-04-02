from unittest.mock import Mock
from collections.abc import Iterator

import pytest

from inbox_client_api import inbox_client_api

"Unit Tests for Client Protocol"


def test_get_messages() -> None:
    """Test get_messages method."""
    client = Mock()
    client.get_messages.return_value = iter([Mock(spec=inbox_client_api.Message)])
    result = client.get_messages()  # Changed from client.id() to client.get_messages()
    assert isinstance(result, Iterator[inbox_client_api.Message])
