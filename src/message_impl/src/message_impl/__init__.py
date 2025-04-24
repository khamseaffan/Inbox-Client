"""Module for the GmailMessage implementation."""

# Import the protocol package
import message

# Import the concrete implementation class from the _impl module
from ._impl import GmailMessage


def get_message_impl(msg_id: str, raw_data: str) -> message.Message:
    """
    Factory function returning an instance of the concrete GmailMessage.

    Args:
        msg_id: The unique identifier for the message.
        raw_data: The raw data used to construct the message.

    Returns:
        message.Message: An instance of GmailMessage conforming to the protocol.
    """
    return GmailMessage(msg_id=msg_id, raw_data=raw_data)


# --- Dependency Injection ---
# Override the get_message function in the protocol package
# Now, anyone calling message.get_message(id, data) will get our implementation.
message.get_message = get_message_impl
# --- Dependency Injection ---
