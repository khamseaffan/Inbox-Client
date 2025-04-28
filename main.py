from prometheus_client import start_http_server
import time
import logging
import os
from dotenv import load_dotenv
import csv

import message
import inbox_client_protocol

import inbox_client_impl
import message_impl

import ai_conversation_client

load_dotenv()

# Configure structured logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    try:
        """Grabs emails and checks spam pct."""
        client = inbox_client_protocol.get_client()
        messages = client.get_messages()
        msg = next(messages)
        msg_id = msg.id
        ai_client = ai_conversation_client.AIConversationClient(
            ai_conversation_client.GeminiAPIClient()
        )
        session_id = ai_client.start_new_session("spam_checker_user")
        
        logging.info("Gemini AI Client initalized successfully.")

        count = 0
        result = {}
        for msg in client.get_messages():
            logging.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")
            count += 1
            message = ("Analyze this email and give me the percent probability it is "
                "spam. Only provide a number. Do not provide any other text."
                "Subject: {msg.subject}, Body: {msg.body}, From: {msg.from_} ")
            response = ai_client.send_message(session_id, message)
            result[msg.id] = response["content"]
            if count >= 5: # Limit for testing
                break
        logging.info(f"Finished fetching and analyzing {count} messages.")
        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Email ID", "Percentage Probability of SPAM"])
            for key,value in result.items():
                numeric_value = ''.join(filter(str.isdigit, str(value)))
                if numeric_value:
                    value = int(numeric_value)
                else:
                    value = 0 # Default value if no digits are found
                writer.writerow([key,value])
        logging.info("Wrote output csv file.")
        ai_client.end_session(session_id)

    except FileNotFoundError as e:
        logging.exception("Initialization failed")
    except RuntimeError as e:
        logging.exception("Credential acquisition failed")


if __name__ == "__main__":
    main()

