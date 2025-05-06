from prometheus_client import start_http_server
import time
import logging
import os
from dotenv import load_dotenv
from inbox_client_impl import GmailClient # Or use inbox_client_protocol.get_client()
import ai_conversation_client

load_dotenv()

# Configure structured logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    """Instantiate the client to trigger auth flow (using .env locally)."""
    logger = logging.getLogger(__name__)
    try:
        # # Initialize Gmail client
        # gmail_client = GmailClient()
        # logger.info("GmailClient initialized successfully.")

        # count = 0
        # for msg in gmail_client.get_messages():
        #     logger.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")
        #     count += 1
        #     if count >= 3: # Limit for testing
        #          break
        # logger.info(f"Finished fetching {count} messages.")

        # Test AI conversation client using dependency injection
        ai_client = ai_conversation_client.get_client()
        logger.info("AI Conversation Client initialized successfully.")

        # Start a new conversation session
        session_id = ai_client.start_new_session(user_id="test_user")
        logger.info(f"Started new AI conversation session with ID: {session_id}")

        # Set preferences for the user
        ai_client.set_user_preferences(
            user_id="test_user",
            preferences={"system_prompt": "You are a helpful AI assistant."}
        )
        logger.info("User preferences set successfully.")

        # Send a test message
        response = ai_client.send_message(session_id, "Do you like apples?")
        logger.info(f"Received AI response: {response['content']}")

    except FileNotFoundError as e:
        logger.exception("Initialization failed")
    except RuntimeError as e:
        logger.exception("Credential acquisition failed")
    except ValueError as e:
        logger.exception("AI client error")

if __name__ == "__main__":
    main()
