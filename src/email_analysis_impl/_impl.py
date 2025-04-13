import re
from prometheus_client import Counter

# Prometheus Counters
emails_processed_total = Counter(
    "emails_processed_total", "Total number of emails processed"
)

emails_classified_as_spam_total = Counter(
    "emails_classified_as_spam_total", "Total number of emails classified as spam"
)

class LLMAnalyzer:
    """
    A mock email analyzer that detects spam and importance using simple keyword rules.
    """

    def analyze(self, email_body: str) -> dict:
        """
        Analyze the email text and return classification.

        Args:
            email_body (str): The body content of the email.

        Returns:
            dict: Contains 'spam' (bool) and 'importance' (str)
        """
        emails_processed_total.inc()  # Increment total emails processed

        lower_body = email_body.lower()
        spam_keywords = ['unsubscribe', 'buy now', 'click here', 'winner', 'free', 'offer']
        is_spam = any(word in lower_body for word in spam_keywords)

        if is_spam:
            emails_classified_as_spam_total.inc()  # Increment spam count

        if re.search(r'\burgent\b|\bimmediately\b|\basap\b', lower_body):
            importance = "high"
        elif re.search(r'\blow priority\b|\bignore\b', lower_body):
            importance = "low"
        else:
            importance = "normal"

        return {
            "spam": is_spam,
            "importance": importance
        }

def get_analyzer() -> LLMAnalyzer:
    return LLMAnalyzer