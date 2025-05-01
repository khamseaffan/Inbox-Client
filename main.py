from prometheus_client import start_http_server
import time
import logging
import os
import csv
import json
import argparse

from dotenv import load_dotenv

import message
import inbox_client_protocol
import inbox_client_impl
import message_impl
import ai_conversation_client

load_dotenv()

# Define default prompt and allow override via CLI or .env
DEFAULT_PROMPT = (
    "Analyze this email and return two things in JSON format:\n"
    "1. The percent probability that this email is spam (integer).\n"
    "2. The tone of the email (e.g., 'formal', 'casual', 'urgent').\n"
    "Return JSON like: {\"pct_spam\": 85, \"tone\": \"formal\"}.\n"
    "Subject: {subject}, Body: {body}, From: {from_}"
)

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze emails using AI")
    parser.add_argument("--limit", type=int, default=5, help="Number of emails to process")
    parser.add_argument("--prompt", type=str, default=None, help="Custom prompt template")
    return parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main() -> None:
    """Main function that fetches emails, checks spam probability and tone, and writes results."""
    args = parse_args()
    limit = args.limit
    prompt_template = args.prompt or os.getenv("AI_PROMPT_TEMPLATE", DEFAULT_PROMPT)

    try:
        client = inbox_client_protocol.get_client()

        try:
            gemini_client = ai_conversation_client.GeminiAPIClient()
            ai_client = ai_conversation_client.AIConversationClient(gemini_client)
        except Exception as e:
            logging.error("Failed to initialize Gemini API client", exc_info=True)
            return

        session_id = ai_client.start_new_session("spam_checker_user")
        logging.info("Gemini AI Client initialized successfully.")

        count = 0
        result = {}

        for msg in client.get_messages():
            logging.info(f"Found message: ID={msg.id}, Subject='{msg.subject}'")

            try:
                prompt = prompt_template.format(
                    subject=msg.subject,
                    body=msg.body,
                    from_=msg.from_,
                )

                response = ai_client.send_message(session_id, prompt)
                content = response["content"]

                parsed = json.loads(content)
                pct_spam = int(parsed.get("pct_spam", 0))
                tone = parsed.get("tone", "unknown")

                result[msg.id] = (pct_spam, tone)

            except Exception as e:
                logging.warning(f"Failed to process message {msg.id}: {e}")
                result[msg.id] = (0, "unknown")

            count += 1
            if count >= limit:
                break

        logging.info(f"Finished fetching and analyzing {count} messages.")

        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Email ID", "Percentage Probability of SPAM", "Tone"])
            for msg_id, (pct_spam, tone) in result.items():
                writer.writerow([msg_id, pct_spam, tone])

        logging.info("Wrote output to output.csv")
        ai_client.end_session(session_id)

    except Exception as e:
        logging.exception("Fatal error occurred.")

if __name__ == "__main__":
    main()
