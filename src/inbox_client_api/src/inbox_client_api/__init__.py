"""Inbox Client API Interface."""

from typing import Protocol
from collections.abc import Iterator
from src.message.src.message import Message

class Client(Protocol):
    """
    Inbox Client Interface Protocol.

    Defines the structure for an inbox client to interact with messages,
    including fetching, sending, deleting, and marking messages as read.
    """

    def get_messages(self) -> Iterator[Message]:
        """
        Retrieve messages from the inbox.

        Returns:
            Iterator[Message]: An iterator over Message objects.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

def get_client() -> Client:
    """
    Return an instance of a Mail Client.

    Returns:
        Client: An instance of the inbox client.

    Raises:
        NotImplementedError: If the method is not implemented.
    """
    raise NotImplementedError
