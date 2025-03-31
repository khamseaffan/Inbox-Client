from unittest.mock import Mock

import pytest

from src.message import src

"Unit Tests for Message Protocol"


def test_id() -> None:
    message = Mock()
    message.id.return_value = str
    result = message.id()
    assert isinstance(result, str)


def test_from() -> None:
    message = Mock()
    message.from_.return_value = str
    result = message.from_()
    assert isinstance(result, str)


def test_to() -> None:
    message = Mock()
    message.to.return_value = str
    result = message.to()
    assert isinstance(result, str)


def test_date() -> None:
    message = Mock()
    message.date.return_value = str
    result = message.date()
    assert isinstance(result, str)


def test_subject() -> None:
    message = Mock()
    message.subject.return_value = str
    result = message.subject()
    assert isinstance(result, str)

def test_body() -> None:
    message = Mock()
    message.body.return_value = str
    result = message.body()
    assert isinstance(result, str)

def test_get_message() -> None:
    message = Mock()
    message.get_message.return_value = src.Message
    result = message.get_message()
    assert isinstance(result, src.Message)
