# Inbox Client Protocol

## Overview

The `Analyzer` protocol defines a standard set of methods for interacting with email messages.

This interface is designed using Python’s `typing.Protocol`, which allows for flexible, type-safe design and easy mocking in tests.

## Scope

The scope of the Analyzer interface is to provide a unified, flexible interface for analysis of email messages. The goal is to support:

- Analyzing a message for spam.
- Analyzing the importance of a message.

The minimum viable version includes:

- Implementing the core method: `analyze`
- Basic error handling and response validation.

### Out of Scope

- Support for non-standard or proprietary messaging protocols.
- Integration with third-party services outside basic email and messaging clients.

## Protocol Definition

The protocol is defined in `__init__.py` and includes the following method:

### `analyze() -> dict`

Returns a dict containing information about email analysis. 

## Usage

To implement this protocol:

1. Import the protocol:

```python
from src.email_analysis import Analyzer
```
