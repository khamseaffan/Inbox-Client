# Inbox Client Protocol

## Overview

The `Client` protocol defines a standard set of methods for interacting with inbox services such as Gmail, Hotmail, or LinkedIn Messaging.

This interface is designed using Python’s `typing.Protocol`, which allows for flexible, type-safe design and easy mocking in tests.


## Protocol Definition
The protocol is defined in `__init__.py` and includes the following methods:

### `get_messages() -> Iterator[Message]`
Returns an iterator over inbox messages. Each message adheres to the `Message` protocol.

### `send_message(to: str, subject: str, body: str) -> bool`
Sends a new message to the specified recipient with a subject and body.

### `delete_message(message_id: str) -> bool`
Deletes the specified message.

### `mark_as_read(message_id: str) -> bool`
Marks the specified message as read.

---

## Message Protocol

The `Message` protocol is defined separately (see the `message` package) and contains:

- `id`: Unique message ID  
- `from_`: Sender address  
- `to`: Recipient address  
- `date`: Timestamp (string format)  
- `subject`: Message subject  
- `body`: Message content

Each of these is exposed via `@property`, making the message read-only and compliant with structural typing.

---

## Usage
To implement this protocol:

1. Import the protocol:
```python
from src.inbox_client_interface import InboxClient
```

2. Create a class that implements the protocol:
```python
class MyClient(InboxClient):
    def fetch_messages(folder: Optional[str] = "inbox") -> Any:
        #implementation here
```

---

## Testing 
Test implementations should use the provided mock fixtures in the test suite.

## Requirements
- Python 3.13 or higher
- No additional dependencies required