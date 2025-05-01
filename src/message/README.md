# Message Protocol

## Overview

The `Message` protocol defines a standard, read-only structure for representing a mail message in inbox clients.

This protocol is intended for use in conjunction with the `Client` protocol defined in the `inbox_client_api` package.

## Scope

The primary scope of the Message Protocol is to provide a unified, immutable representation of an inbox message. The project aims to standardize message attributes across different inbox client implementations.

The minimum viable version includes:

- Defining core attributes such as `id`, `from_`, `to`, `date`, `subject`, and `body`.
- Ensuring read-only access to all message fields.
- Compatibility with multiple inbox client APIs through a consistent interface.

### Out of Scope

- Modifying message content directly through the protocol.
- Handling complex message parsing, such as multimedia content or message threading.
- Providing advanced features like automatic message classification or spam detection.

## Protocol Definition

The `Message` protocol is defined using `typing.Protocol`, allowing for flexible structural subtyping and compatibility with `mypy` and test mocks.

### Properties

| Property  | Type  | Description                                                   |
| --------- | ----- | ------------------------------------------------------------- |
| `id`      | `str` | Unique identifier of the message                              |
| `from_`   | `str` | Sender email address                                          |
| `to`      | `str` | Recipient email address                                       |
| `date`    | `str` | Timestamp of when the message was sent (ISO or string format) |
| `subject` | `str` | Subject line of the message                                   |
| `body`    | `str` | Body content of the message                                   |

All attributes are exposed as **read-only properties**, ensuring that message objects are immutable from the interface perspective.

## Usage Example

The `Message` protocol is used to provide a consistent interface across implementations.

```python
from message import Message

def summarize_email(msg: Message) -> str:
    return f"[{msg.date}] {msg.from_} -> {msg.to}: {msg.subject}"
```
