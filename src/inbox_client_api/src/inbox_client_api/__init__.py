"""Inbox Client API Interface."""

from typing import Protocol
from collections.abc import Iterator
from src.message.src.message import Message


class Client(Protocol):
    """Inbox Client Interface Protocol."""

    def get_messages(self) -> Iterator[Message]:
        """Return an iterator of messages."""
        raise NotImplementedError

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """Send a message."""
        raise NotImplementedError

    def delete_message(self, message_id: str) -> bool:
        """Delete a message."""
        raise NotImplementedError

    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read."""
        raise NotImplementedError


def get_client() -> Client:
    """Return an instance of a Mail Client."""
    raise NotImplementedError
