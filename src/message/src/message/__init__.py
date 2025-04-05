"""Unit Tests for mockedMessage Protocol."""

from typing import Protocol, runtime_checkable
from collections.abc import Iterator

@runtime_checkable
class Message(Protocol):
    """
    A Mail Message Interface.

    Represents the structure of a message object with essential attributes.
    """

    @property
    def id(self) -> str:
        """
        Retrieve the unique ID of the message.

        Returns:
            str: The message ID.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    def from_(self) -> str:
        """
        Retrieve the sender's address.

        Returns:
            str: The email address of the sender.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    def to(self) -> str:
        """
        Retrieve the recipient's address.

        Returns:
            str: The email address of the recipient.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    def date(self) -> str:
        """
        Retrieve the date the message was sent.

        Returns:
            str: The date in 'MM/DD/YYYY' format.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    def subject(self) -> str:
        """
        Retrieve the subject of the message.

        Returns:
            str: The subject line.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @property
    def body(self) -> str:
        """
        Retrieve the body of the message.

        Returns:
            str: The message content.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

def get_message() -> Message:
    """
    Return an instance of a Message.

    Returns:
        Message: An instance of a message object.

    Raises:
        NotImplementedError: If the method is not implemented.
    """
    raise NotImplementedError
