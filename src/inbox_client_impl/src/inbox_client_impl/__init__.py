"""Module for the GmailClient implementation."""

# Import the protocol package
import inbox_client_protocol

# Import the concrete implementation class from the _impl module
from ._impl import GmailClient

def get_client_impl(interactive: bool = False) -> inbox_client_protocol.Client:
    """Factory function to return an instance of the inbox client."""
    # Dynamically import the implementation to avoid circular dependencies
    # and allow for different implementations in the future.
    try:
        # Assuming the implementation package is installed or in the path
        import inbox_client_impl
        # Pass the interactive flag to the implementation's constructor
        return GmailClient(interactive=interactive)
    except ImportError as e:
        print(f"Error importing inbox client implementation: {e}")
        raise


# --- Dependency Injection ---
# Override the get_client function in the protocol package
# Now, anyone calling inbox_client_protocol.get_client() will get our implementation.
inbox_client_protocol.get_client = get_client_impl
# --- Dependency Injection ---
