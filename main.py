from prometheus_client import start_http_server
import time
import logging
import os
from dotenv import load_dotenv
from inbox_client_impl import GmailClient # Or use inbox_client_protocol.get_client()

load_dotenv()

# Configure structured logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    """Instantiate the client to trigger auth flow (using .env locally)."""
    logger = logging.getLogger(__name__)
    try:
        client = GmailClient()
        logger.info("GmailClient initialized successfully.")

        count = 0
        for msg in client.get_messages():
            logger.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")
            count += 1
            if count >= 3: # Limit for testing
                 break
        logger.info(f"Finished fetching {count} messages.")

    except FileNotFoundError as e:
        logger.exception("Initialization failed")
    except RuntimeError as e:
        logger.exception("Credential acquisition failed")

if __name__ == "__main__":
    main()
