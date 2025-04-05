# Inbox Client Protocol

## Overview

The `Client` protocol defines a standard set of methods for interacting with inbox services such as Gmail, Hotmail, or LinkedIn Messaging.

This interface is designed using Python’s `typing.Protocol`, which allows for flexible, type-safe design and easy mocking in tests.

## Scope

The scope of the Inbox Client API project is to provide a unified, flexible interface for inbox client applications. The goal is to support:

- Retrieving messages from various inbox services.
- Sending messages to specified recipients.
- Managing messages by deleting or marking them as read.

The minimum viable version includes:

- Implementing the core methods: `get_messages`, `send_message`, `delete_message`, and `mark_as_read`.
- Basic error handling and response validation.

### Out of Scope

- Support for non-standard or proprietary messaging protocols.
- Advanced message filtering and search capabilities.
- Integration with third-party services outside basic email and messaging clients.

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

## Message Protocol

The `Message` protocol is defined separately (see the `message` package) and contains:

- `id`: Unique message ID
- `from_`: Sender address
- `to`: Recipient address
- `date`: Timestamp (string format)
- `subject`: Message subject
- `body`: Message content

Each of these is exposed via `@property`, making the message read-only and compliant with structural typing.

## Usage

To implement this protocol:

1. Import the protocol:

```python
from src.inbox_client_interface import InboxClient
```
