"""Inbox Client API Interface."""

from typing import Protocol
from collections.abc import Iterator
# Use the package name directly for imports within the workspace
from message import Message

class Client(Protocol):
    """Define base class for interacting with an inbox client."""

    def get_messages(self) -> Iterator[Message]:
        """Retrieve messages from the inbox."""
        raise NotImplementedError

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """
        Send a message.

        Args:
            to (str): Recipient email address.
            subject (str): Subject line.
            body (str): Message body.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented.

        """
        raise NotImplementedError

    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message by its ID.

        Args:
            message_id (str): The unique ID of the message to delete.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented.

        """
        raise NotImplementedError

    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read by its ID.

        Args:
            message_id (str): The unique ID of the message to mark as read.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented.

        """
        raise NotImplementedError

def get_client(interactive: bool = False) -> Client: # noqa: FBT002 FBT001
    """
    Return an instance of a Mail Client.

    Returns:
        Client: An instance of the inbox client.

    Raises:
        NotImplementedError: If the method is not implemented.

    """
    raise NotImplementedError
