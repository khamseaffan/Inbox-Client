"""Unit Tests for mockedMessage Protocol."""

from typing import Protocol, runtime_checkable
from collections.abc import Iterator

@runtime_checkable
class Message(Protocol):
    """A Mail Message."""

    @property
    def id(self) -> str:
        """Return the id of the message."""
        raise NotImplementedError

    @property
    def from_(self) -> str:
        """Return the sender of the message."""
        raise NotImplementedError

    @property
    def to(self) -> str:
        """Return the recipient of the message."""
        raise NotImplementedError

    @property
    def date(self) -> str:
        """Return the date of the message."""
        raise NotImplementedError

    @property
    def subject(self) -> str:
        """Return the subject of the message."""
        raise NotImplementedError

    @property
    def body(self) -> str:
        """Return the body of the message."""
        raise NotImplementedError

def get_message() -> Message:
    """Return an instance of a Mail Client."""
    raise NotImplementedError

