from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from src.message.src.message import Message

if TYPE_CHECKING:
    from message import Message

"Unit Tests for mockedMessage Protocol"

def test_id() -> None:
    """Test id method."""
    mockedMessage: Message = Mock()
    mockedMessage.id.return_value = "123"
    result = mockedMessage.id()
    assert isinstance(result, str)


def test_from() -> None:
    """Test from method."""
    mockedMessage: Message = Mock()
    mockedMessage.from_.return_value = "John"
    result = mockedMessage.from_()
    assert isinstance(result, str)


def test_to() -> None:
    """Test to method."""
    mockedMessage: Message = Mock()
    mockedMessage.to.return_value = "Sally"
    result = mockedMessage.to()
    assert isinstance(result, str)


def test_date() -> None:
    """Test date method."""
    mockedMessage: Message = Mock()
    mockedMessage.date.return_value = "10/1/2020"
    result = mockedMessage.date()
    assert isinstance(result, str)


def test_subject() -> None:
    """Test subject method."""
    mockedMessage: Message = Mock()
    mockedMessage.subject.return_value = "Work"
    result = mockedMessage.subject()
    assert isinstance(result, str)

def test_body() -> None:
    """Test body method."""
    mockedMessage: Message = Mock()
    mockedMessage.body.return_value = "We need to meet"
    result = mockedMessage.body()
    assert isinstance(result, str)

