from unittest.mock import Mock
from typing import Iterator

import pytest

from src.inbox_client_api import src

"Unit Tests for Client Protocol"


def test_get_messages() -> None:
    client = Mock()
    client.get_messages.return_value = Iterator[src.Message]
    result = client.id()
    assert isinstance(result, Iterator[src.Message])
