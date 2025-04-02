from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from message import message

if TYPE_CHECKING:
    from message import message

"Unit Tests for mockedMessage Protocol"

def test_id() -> None:
    """Test id method."""
    mockedMessage: message = Mock()
    mockedMessage.id.return_value = str
    result = mockedMessage.id()
    assert isinstance(result, str)


def test_from() -> None:
    """Test from method."""
    mockedMessage: message = Mock()
    mockedMessage.from_.return_value = str
    result = mockedMessage.from_()
    assert isinstance(result, str)


def test_to() -> None:
    """Test to method."""
    mockedMessage: message = Mock()
    mockedMessage.to.return_value = str
    result = mockedMessage.to()
    assert isinstance(result, str)


def test_date() -> None:
    """Test date method."""
    mockedMessage: message = Mock()
    mockedMessage.date.return_value = str
    result = mockedMessage.date()
    assert isinstance(result, str)


def test_subject() -> None:
    """Test subject method."""
    mockedMessage: message = Mock()
    mockedMessage.subject.return_value = str
    result = mockedMessage.subject()
    assert isinstance(result, str)

def test_body() -> None:
    """Test body method."""
    mockedMessage: message = Mock()
    mockedMessage.body.return_value = str
    result = mockedMessage.body()
    assert isinstance(result, str)

def test_get_mocked_message() -> None:
    """Test get_mocked_message method."""
    mockedMessage: message = Mock()
    mockedMessage.get_mockedMessage.return_value = mockedMessage.mockedMessage
    result = mockedMessage.get_mockedMessage()
    assert isinstance(result, mockedMessage.mockedMessage)
