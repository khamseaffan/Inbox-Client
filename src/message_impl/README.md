# Gmail Message Implementation (`message_impl`)

## Overview

This package provides `GmailMessage`, a concrete implementation of the `Message` protocol defined in the `message` package. It is specifically designed to parse raw email data obtained from the Google Gmail API (typically base64url-encoded strings) using Python's standard `email` library to extract standard message properties.

## Features

- Implements all properties defined in the `Message` protocol:
  - `id`: Unique message identifier.
  - `from_`: Sender address.
  - `to`: Recipient address.
  - `date`: Message date, formatted as `MM/DD/YYYY` where possible.
  - `subject`: Message subject, with support for decoding RFC 2047 encoded headers.
  - `body`: Plain text message body, extracted even from multipart messages.
- Parses standard email headers using `email.message.EmailMessage`.
- Handles basic multipart messages, prioritizing the `text/plain` part for the `body` property.
- Includes basic error handling for invalid base64 input or email parsing errors, setting default values for properties in case of failure.
- Provides fallback mechanisms for date formatting and subject decoding if errors occur.

## Usage (Dependency Injection)

This package utilizes a dependency injection pattern. Upon import, its `__init__.py` overrides the `get_message()` factory function originally defined in the `message` protocol package.

Client implementations (like `GmailClient` in `inbox_client_impl`) should **use the protocol's factory function** to create message objects. This ensures that the client code remains decoupled from the specific message implementation details.

```python
# Example within a Client implementation (e.g., GmailClient.get_messages)
import message
# Import the implementation package (this performs the factory override)
import message_impl

# ... fetch raw_content and msg_summary['id'] from API ...

# Use the factory from the 'message' protocol package.
# Due to the override, this will call message_impl.get_message_impl
# and return an instance of GmailMessage.
msg_object: message.Message = message.get_message(
    msg_id=msg_summary['id'],
    raw_data=raw_content
)
yield msg_object
```

Direct instantiation of `GmailMessage` is possible but generally discouraged outside of testing or specific internal use cases, as it bypasses the intended decoupling provided by the protocol and factory pattern.

## Dependencies

- `message` (workspace package): Provides the `Message` protocol that `GmailMessage` implements.
