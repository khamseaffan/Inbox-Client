from prometheus_client import start_http_server
import time
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def main() -> None:
    """Start the Prometheus metrics server and run app logic."""
    logging.info("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)

    logging.info("Hello from inbox-client! Monitoring is live.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.warning("Shutting down.")

if __name__ == "__main__":
    main()
