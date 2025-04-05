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

    def send_message(self, to: str, subject: str, body: str) -> bool:
        """
        Send a message to the specified recipient.

        Parameters:
            to (str): The email address of the recipient.
            subject (str): The subject line of the message.
            body (str): The content of the message.

        Returns:
            bool: True if the message was sent successfully, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message by its unique identifier.

        Parameters:
            message_id (str): The unique ID of the message to be deleted.

        Returns:
            bool: True if the message was deleted successfully, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read using its unique identifier.

        Parameters:
            message_id (str): The unique ID of the message to be marked as read.

        Returns:
            bool: True if the message was successfully marked as read, False otherwise.

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
