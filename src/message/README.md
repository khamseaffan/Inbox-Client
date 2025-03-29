# Message Protocol

## Overview

The `Message` protocol defines a standard, read-only structure for representing a mail message in inbox clients. 

This protocol is intended for use in conjunction with the `Client` protocol defined in the `inbox_client_api` package.

---

## Protocol Definition

The `Message` protocol is defined using `typing.Protocol`, allowing for flexible structural subtyping and compatibility with `mypy` and test mocks.

### Properties

| Property   | Type   | Description                          |
|------------|--------|--------------------------------------|
| `id`       | `str`  | Unique identifier of the message     |
| `from_`    | `str`  | Sender email address                 |
| `to`       | `str`  | Recipient email address              |
| `date`     | `str`  | Timestamp of when the message was sent (ISO or string format) |
| `subject`  | `str`  | Subject line of the message          |
| `body`     | `str`  | Body content of the message          |

All attributes are exposed as **read-only properties**, ensuring that message objects are immutable from the interface perspective.
