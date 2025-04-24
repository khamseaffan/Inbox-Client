"""Protocol for a Mail Message."""

from typing import Protocol, runtime_checkable

# Removed Iterator import as it's not used here
# from collections.abc import Iterator


@runtime_checkable
class Message(Protocol):
    """
    A Mail Message Interface.

    Represents the structure of a message object with essential attributes.
    All properties are intended to be read-only from the protocol perspective.
    """

    @property
    def id(self) -> str:
        """
        Retrieve the unique ID of the message.

        Returns:
            str: The message ID.

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError

    @property
    def from_(self) -> str:
        """
        Retrieve the sender's address.

        Returns:
            str: The email address of the sender.

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError

    @property
    def to(self) -> str:
        """
        Retrieve the recipient's address.

        Returns:
            str: The email address of the recipient.

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError

    @property
    def date(self) -> str:
        """
        Retrieve the date the message was sent.

        Returns:
            str: The date, ideally formatted (e.g., 'MM/DD/YYYY'),
                 but could be the raw string.

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError

    @property
    def subject(self) -> str:
        """
        Retrieve the subject of the message.

        Returns:
            str: The subject line.

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError

    @property
    def body(self) -> str:
        """
        Retrieve the body of the message.

        Returns:
            str: The message content (typically plain text).

        Raises:
            NotImplementedError: If the property is not implemented.
        """
        raise NotImplementedError


# --- Factory Function ---
# Modified signature to accept parameters needed by the implementation
def get_message(msg_id: str, raw_data: str) -> Message:
    """
    Factory function to return an instance of a Message.

    Args:
        msg_id: The unique identifier for the message.
        raw_data: The raw data used to construct the message.

    Returns:
        Message: An instance conforming to the Message protocol.

    Raises:
        NotImplementedError: If the function is not overridden by an implementation.
    """
    raise NotImplementedError

