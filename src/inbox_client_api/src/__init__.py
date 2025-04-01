from typing import Iterator, Protocol
from message import Message

class Client(Protocol):
    """Inbox Client Interface Protocol."""

    def get_messages(self) -> Iterator[Message]:
        raise NotImplementedError()

    def send_message(self, to: str, subject: str, body: str) -> bool:
        raise NotImplementedError()

    def delete_message(self, message_id: str) -> bool:
        raise NotImplementedError()

    def mark_as_read(self, message_id: str) -> bool:
        raise NotImplementedError()


def get_client() -> Client:
    """Return an instance of a Mail Client."""
    raise NotImplementedError()