import time
import logging
import os
import csv
from dotenv import load_dotenv
from inbox_client_impl import GmailClient # Or use inbox_client_protocol.get_client()
from ai_client_impl import GeminiAPIClient

load_dotenv()

# Configure structured logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    """Instantiate the client to trigger auth flow (using .env locally)."""
    logger = logging.getLogger(__name__)
    try:
        client = GmailClient()
        logger.info("GmailClient initialized successfully.")
        ai_client = GeminiAPIClient()
        session_id = ai_client.start_new_session("test_user")
        logger.info("Gemini AI Client initalized successfully.")
        count = 0
        result = {}
        for msg in client.get_messages():
            logger.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")
            count += 1
            message = (f"Analyze this email and give me the percent probability it is spam: Subject: {msg.subject}, Body: {msg.body}, From: {msg.from_} ")
            response = ai_client.send_message(session_id, message)
            result[msg.id] = response["content"]
            if count >= 5: # Limit for testing
                 break
        logger.info(f"Finished fetching and analyzing {count} messages.")
        with open('output.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Email ID", "Percentage Probability of SPAM"])
            for key,value in result.items():
                writer.writerow([key,value])
        logger.info("Wrote output csv file.")

    except FileNotFoundError as e:
        logger.exception("Initialization failed")
    except RuntimeError as e:
        logger.exception("Credential acquisition failed")

if __name__ == "__main__":
    main()
