"""Main entry point for the inbox-client application."""

from prometheus_client import start_http_server
import time

def main() -> None:
    """Start the Prometheus metrics server and run app logic."""
    print("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)

    print("Hello from inbox-client! Monitoring is live.")

    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("Shutting down.")


if __name__ == "__main__":
    """Main function runs the inbox-client application."""
    main()
