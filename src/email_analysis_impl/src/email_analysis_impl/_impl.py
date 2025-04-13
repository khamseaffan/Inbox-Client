import re
import time
import logging
from prometheus_client import Counter, Histogram

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Prometheus Counters
emails_analyzed_total = Counter(
    "emails_analyzed_total", "Total number of emails analyzed"
)
emails_processed_total = Counter(
    "emails_processed_total", "Total number of emails processed"
)

emails_classified_as_spam_total = Counter(
    "emails_classified_as_spam_total", "Total number of emails classified as spam"
)

emails_marked_high_importance_total = Counter(
    "emails_marked_high_importance_total", "Total number of emails marked high importance"
)

email_analysis_duration_seconds = Histogram(
    "email_analysis_duration_seconds", "Time spent analyzing each email"
)

class LLMAnalyzer:
    """
    A mock email analyzer that detects spam and importance using simple keyword rules.
    """
    def __init__(self):
        self.spam_keywords = re.compile(r"(buy now|free money|click here|winner|act now)", re.IGNORECASE)
        self.important_keywords = re.compile(r"(meeting|schedule|urgent|asap)", re.IGNORECASE)

    def analyze(self, email_body: str) -> dict:
        """
        Analyze an email body and classify it as spam/important.

        Args:
            email_body (str): Raw text of the email.

        Returns:
            dict: {
                "is_spam": bool,
                "importance": "high" or "normal" or "low"
            }
        """
        start_time = time.time()
        emails_processed_total.inc()
        emails_analyzed_total.inc()

        # Lowercase for easier keyword matching
        lower_body = email_body.lower()

        # Spam keyword match (simple list + regex)
        spam_keywords = ['unsubscribe', 'buy now', 'click here', 'winner', 'free', 'offer', 'act now']
        is_spam = bool(self.spam_keywords.search(email_body)) or any(word in lower_body for word in spam_keywords)

        if is_spam:
            emails_classified_as_spam_total.inc()
            logging.info("Email classified as SPAM.")

        # Importance detection (high, low, normal)
        if re.search(r'\burgent\b|\bimmediately\b|\basap\b', lower_body) or self.important_keywords.search(email_body):
            importance = "high"
            emails_marked_high_importance_total.inc()
            logging.info("Email marked as HIGH importance.")
        elif re.search(r'\blow priority\b|\bignore\b', lower_body):
            importance = "low"
            logging.info("Email marked as LOW importance.")
        else:
            importance = "normal"
            logging.info("Email marked as NORMAL importance.")

        # Observe analysis time
        duration = time.time() - start_time
        email_analysis_duration_seconds.observe(duration)
        logging.info(f"Email analysis took {duration:.4f} seconds.")

        return {
            "is_spam": is_spam,
            "importance": importance
        }

def get_analyzer() -> LLMAnalyzer:
    return LLMAnalyzer()