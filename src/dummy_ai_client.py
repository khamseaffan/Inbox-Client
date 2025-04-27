import random

class DummyAIClient:
    """Fake AI client that returns random spam probability."""

    def analyze_email(self, email_body):
        """Return a random spam probability for a given email body."""
        return random.uniform(0, 100)  # Random float between 0 and 100