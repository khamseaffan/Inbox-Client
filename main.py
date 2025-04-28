from prometheus_client import start_http_server
import time
import logging
import os
from dotenv import load_dotenv


import message
import inbox_client_protocol

import inbox_client_impl
import message_impl

import ai_conversation_client

load_dotenv()

# Configure structured logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    client = inbox_client_protocol.get_client()
    messages = client.get_messages()
    msg = next(messages)
    msg_id = msg.id
    ai_client = ai_conversation_client.AIConversationClient(
        ai_conversation_client.GeminiAPIClient()
    )
    session_id = ai_client.start_new_session("spam_checker_user")

    print(ai_client.send_message(message="Hello, how are you?", session_id=session_id).values())

    # for message in messages:
    #     logging.info(f"Message ID: {message.id}")
    #     logging.info(f"Message Body: {message.body}")
    #     logging.info(f"Message Subject: {message.subject}")
    #     logging.info(f"Message Date: {message.date}")
    return

if __name__ == "__main__":
    main()

