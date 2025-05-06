# AI Conversation Client Component

## Concept of a Component

In software architecture, a **component** is a modular, reusable, and encapsulated unit of functionality that performs a specific task or a closely related set of tasks. It interacts with other components only through well-defined interfaces and is designed to be independently tested, maintained, or replaced.

In this repository, a component adheres to this principle by organizing its logic, interfaces, and models in a self-contained folder. This promotes code readability, reusability, testability, and separation of concerns.

---

## Directory Structure

```
ai_conversation_client/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Implementation of AIConversationClient class
│   ├── interface.py             # Abstract interface for conversation clients
│   ├── conversation.py          # Models for Message and Conversation objects
│   ├── gemini_api_client.py     # Gemini API implementation of the conversation client
│   └── cli.py                   # Command-line interface for the client

tests/
│   ├── test_client.py           # Unit tests for AIConversationClient
│   └── dummy_api_client.py      # Dummy client used for testing
```

Each component follows a structure where:
- **Implementation file** (`client.py`): Contains the core client logic and delegates to the API client.
- **Interface file** (`interface.py`): Defines the interface for interchangeable API clients.
- **Models file** (`conversation.py`): Defines `Message` and `Conversation` data models.
- **API Client** (`gemini_api_client.py`): Implementation using Google's Gemini API.
- **CLI Tool** (`cli.py`): Enables terminal-based interaction for testing and development.

For tests:
- **Test file** (`test_client.py`): Contains test cases to validate behavior.
- **Dummy API client** (`dummy_api_client.py`): A mock implementation for isolated testing.

---

## AIConversationClient Component

### Purpose

The `AIConversationClient` component handles AI conversation sessions. It provides methods for sending messages, retrieving chat history, setting user preferences, and managing session lifecycles. This component interacts with an external API client (passed via dependency injection), ensuring decoupling and flexibility.

### Methods and Inputs/Outputs

- **send_message(session_id: str, message: str) -> dict[str, Any]**  
  Sends a message to the API client and retrieves the response.  
  **Input:** `session_id` (str), `message` (str)  
  **Output:** `response` (dict)

- **get_chat_history(session_id: str) -> list[dict[str, Any]]**  
  Retrieves the chat history for a given session.  
  **Input:** `session_id` (str)  
  **Output:** `chat_history` (list of dict)

- **set_user_preferences(user_id: str, preferences: dict[str, Any]) -> bool**  
  Sets user preferences via the API client.  
  **Input:** `user_id` (str), `preferences` (dict)  
  **Output:** `success` (bool)

- **start_new_session(user_id: str) -> str**  
  Starts a new conversation session for a given user.  
  **Input:** `user_id` (str)  
  **Output:** `session_id` (str)

- **end_session(session_id: str) -> bool**  
  Ends the specified session.  
  **Input:** `session_id` (str)  
  **Output:** `success` (bool)

---

### Example Usage

```python
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

api_client = GeminiAPIClient()
conversation_client = AIConversationClient(api_client)

session_id = conversation_client.start_new_session("user_123")
response = conversation_client.send_message(session_id, "Hello, AI!")
chat_history = conversation_client.get_chat_history(session_id)
conversation_client.set_user_preferences("user_123", {"theme": "dark"})
conversation_client.end_session(session_id)
```

### Interactions

The `AIConversationClient` uses an abstract API interface to handle operations. Different implementations (e.g., Gemini, Dummy) can be injected, making testing and future migration easy.

---

## Component Interaction and Integration

The AIConversationClient is designed to be modular and pluggable, enabling:
- Loose coupling between business logic and backend services.
- Straightforward testing using `DummyAPIClient`.
- CLI-based interaction for experimentation or internal tooling.

### Optional Integrations
- **Logger:** Could log every session and message event.
- **Notifier:** Could notify users about session updates or AI-generated alerts.
