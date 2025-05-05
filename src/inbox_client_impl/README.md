# Gmail Inbox Client Implementation (`inbox_client_impl`)

## Overview

This package provides `GmailClient`, a concrete implementation of the `Client` protocol defined in the `inbox_client_protocol` package. It uses the Google Gmail API via the `google-api-python-client` library to interact with a user's Gmail account.

## Features

- Implements all methods defined in the `Client` protocol:
  - `get_messages`
  - `send_message`
  - `delete_message`
  - `mark_as_read`
- Handles OAuth 2.0 authentication using either:
  - Environment variables (`GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`) suitable for CI/server environments.
  - Local file-based flow (`credentials.json`, `token.json`) for initial setup and local development.
- Uses the `Message` protocol and the `GmailMessage` implementation from the `message_impl` package to represent emails.

## Setup & Authentication

This implementation requires Google API credentials.

1. **Google Cloud Setup**  
   Enable the Gmail API in your Google Cloud project and download `credentials.json` (OAuth Client ID for Desktop App).

2. **Local**
   - Place `credentials.json` in the project root.
   - Run the application once; it will trigger a browser-based OAuth flow to generate `token.json`.
   - **(Recommended)** Create a `.env` file in the project root and add:
     - `GMAIL_CLIENT_ID`
     - `GMAIL_CLIENT_SECRET` (from `credentials.json`)
     - `GMAIL_REFRESH_TOKEN` (from `token.json`)
   - Ensure `.env` is listed in `.gitignore`.
   - The application will prioritize these environment variables if `python-dotenv` is used.

3. **CI/Server**
   - Set the `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN` environment variables securely (e.g., using CircleCI Contexts).
   - The code will automatically use these if detected.

## Usage (Dependency Injection)

This package overrides the `get_client()` factory function from the `inbox_client_protocol` package upon import. Consumers should use the protocol's factory:

```python
# Import the protocol package
import inbox_client_protocol
# Import the implementation package (this performs the override)
import inbox_client_impl

# Get the client instance (this will be a GmailClient)
client = inbox_client_protocol.get_client()

# Use the client
messages = client.get_messages()
# ...
```

## Dependencies

- `inbox-client-protocol` (workspace package)
- `message` (workspace package)
- `message-impl` (workspace package)
- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `python-dotenv` (optional, for loading `.env` locally)