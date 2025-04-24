from prometheus_client import start_http_server
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure structured logging
from inbox_client_impl import GmailClient # Or use inbox_client_protocol.get_client()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    """Instantiate the client to trigger auth flow (using .env locally)."""
    try:
        client = GmailClient()
        logging.info("GmailClient initialized successfully.")

        count = 0
        for msg in client.get_messages():
            logging.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")
            count += 1
            if count >= 3: # Limit for testing
                 break
        logging.info(f"Finished fetching {count} messages.")

    except FileNotFoundError as e:

        logging.error(f"Initialization failed: {e}")
    except RuntimeError as e:

        logging.error(f"Credential acquisition failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
