"""Module for the GmailClient implementation."""

# Import the protocol package
import inbox_client_protocol

# Import the concrete implementation class from the _impl module
from ._impl import GmailClient


def get_client_impl() -> inbox_client_protocol.Client:
    """Factory function returning an instance of the concrete GmailClient."""
    return GmailClient(service=None)


# --- Dependency Injection ---
# Override the get_client function in the protocol package
# Now, anyone calling inbox_client_protocol.get_client() will get our implementation.
inbox_client_protocol.get_client = get_client_impl
# --- Dependency Injection ---
