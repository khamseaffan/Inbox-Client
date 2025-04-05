# Inbox Client Workspace

# Description

This repository defines a modular protocol-based interface and implementation for Gmail clients. It uses Python `Protocol` classes to describe standardized, mockable interfaces for both messages and inbox clients.

### Scope

This inbox client is designed to read and parse messages from Gmail, with the capability to perform basic analysis (e.g., sorting by priority and detecting phishing). The **minimum viable product (MVP)** for this client will include the ability to read and return messages from a Gmail account.

#### Implemented Features:

- Reading and returning messages from Gmail.
- Fetching a message by ID.
- Sending a message to a specified recipient.
- Deleting a message by its unique identifier.
- Marking a message as read.
- Basic parsing and analysis of messages (e.g., priority sorting, phishing detection).

#### Out of Scope:

- Parsing messages from non-Gmail services (e.g., Hotmail, LinkedIn).
- Advanced inbox search functionality.
- Handling of attachments within messages.
- Spam detection and filtering.
- Real-time message streaming or push notifications.
- Integration with email clients other than Gmail.

### API Methods

The API defines the following methods for interacting with the inbox client:

| Method                                           | Parameters                                  | Return Type         | Description                                 |
| ------------------------------------------------ | ------------------------------------------- | ------------------- | ------------------------------------------- |
| `get_messages()`                                 | None                                        | `Iterator[Message]` | Fetches all messages from the inbox.        |
| `send_message(to: str, subject: str, body: str)` | Recipient email, subject line, message body | `bool`              | Sends a message to the specified recipient. |
| `delete_message(message_id: str)`                | Unique message ID                           | `bool`              | Deletes the specified message.              |
| `mark_as_read(message_id: str)`                  | Unique message ID                           | `bool`              | Marks the specified message as read.        |

### Usage

#### Reading Messages

```python
from src.inbox_client_api import get_client

client = get_client()
messages = client.get_messages()
for message in messages:
    print(f"From: {message.from_} - Subject: {message.subject}")
```

#### Sending a Message

```python
result = client.send_message("recipient@example.com", "Hello", "This is a test message.")
if result:
    print("Message sent successfully.")
else:
    print("Failed to send message.")
```

#### Deleting a Message

```python
delete_result = client.delete_message("12345")
if delete_result:
    print("Message deleted.")
else:
    print("Failed to delete message.")
```

#### Marking a Message as Read

```python
mark_result = client.mark_as_read("12345")
if mark_result:
    print("Message marked as read.")
else:
    print("Failed to mark as read.")
```

### Requirements

- Python 3.10 or higher
- `pytest` for testing
- `mypy` for type checking
- `ruff` for linting
- `uv` (for dependency and workspace management)
- `coverage`

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/khamseaffan/Inbox-Client.git
   cd Inbox-Client
   ```

2. Install UV, the package manager for dependency management:

   - For macOS/Linux:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - For Windows:
     ```bash
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. Install the project dependencies:
   ```bash
   uv sync
   uv sync --all-packages --extra dev --extra test
   ```

### Testing

To run all of the test suite at once:

```bash
pytest .
```

To run individual test files:

```bash
pytest <path-to-specific-test-file>
```

To run individual tests within a file:

```bash
pytest <path-to-specific-test-file::name-of-individual-test>
```

### Contributions

We welcome any and all contributions and will be using GitHub to track bugs, feature requests, and pull requests.  
By contributing, you agree that your contributions will be licensed under the project's license.

#### Bug Reports and Feature Requests

Use the provided templates to report any bugs and request new features. Please follow the templates accurately to help us understand and more efficiently address your issue.

#### Pull Requests

When submitting a pull request:

- Use the pull request template provided in the repository and follow its instructions.

### License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

### Additional Information

- This project uses CircleCI for continuous integration, which automatically runs tests and checks code formatting with ruff.
- The `.gitignore` file is configured to ignore Python-specific files and directories, such as `__pycache__` and the `venv` directory.
