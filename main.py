"""Main entry point for the inbox-client application."""
from prometheus_client import start_http_server
# import inbox_client_api 
# import email_analysis_api

from src.inbox_client_impl.src.inbox_client_impl._impl import get_client 
from src.email_analysis_impl.src.email_analysis_impl._impl import get_analyzer
from src.message_impl.src.message_impl._impl import GmailMessage
import time
import sys
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def run_analysis():
    """Fetches messages from the inbox client and runs email analysis on them."""
    print("Getting client and analyzer instances...")
    try:
        
        analyzer = get_analyzer()
        logging.info("Analyzer instance obtained successfully.")
        client = get_client()
        
        print("Instances obtained successfully.")
    except Exception as e:
        import traceback
        print(f"Error getting instances: Type={type(e).__name__}, Message='{e}'", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return

    print("\nFetching messages...")
    try:
        messages = client.get_messages()
        logging.info(f"Fetched \n{messages} \nmessages successfully.")
        print("Processing messages:")
        message_count = 0
        for msg in messages:
            message_count += 1
            try:
                print(f"\n--- Message {message_count} ---")
                print(f"  ID: {msg.id}")
                print(f"  From: {msg.from_}")
                print(f"  To: {msg.to}")
                print(f"  Date: {msg.date}")
                print(f"  Subject: {msg.subject}")

                body = msg.body
                if body:
                    print("  Analyzing body...")
                    analysis_result = analyzer.analyze(body)
                    print(f"  Analysis: Spam={analysis_result.get('spam')}, Importance={analysis_result.get('importance')}")
                else:
                    print("  Body is empty, skipping analysis.")

            except NotImplementedError:
                print(f"  Error: A property (like body) might not be implemented for message ID {msg.id}", file=sys.stderr)
            except Exception as e:
                print(f"  Error processing message ID {msg.id}: {e}", file=sys.stderr)

        if message_count == 0:
            print("No messages found or fetched.")

    except NotImplementedError:
         print("Error: get_messages() is not implemented in the client.", file=sys.stderr)
    except Exception as e:
        print(f"\nError during message fetching or processing: {e}", file=sys.stderr)


def main() -> None:
    """Start the Prometheus metrics server and run app logic."""
    logging.info("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)

    logging.info("Hello from inbox-client! Monitoring is live.")
    logging.info("Running email analysis...")

    run_analysis() 

    logging.info("Analysis complete. Monitoring is live.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.warning("Shutting down.")

if __name__ == "__main__":
    main()
