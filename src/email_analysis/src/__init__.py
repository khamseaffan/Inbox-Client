"""Message Analyzer Protocol"""

from typing import Protocol

class Analyzer(Protocol):
    """
    An email analyzer protocol.

    Defines the structure for email analyzer to parse given messages,
    """

    def analyze(self, email: str) -> dict:
        """
        Perform analysis on a given email.

        Args:
            email (str): The given email to analyze. 

        Returns:
            dict: A dict of information about the email.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

def get_analyzer() -> Analyzer:
    """
    Return an instance of an email analyzer.

    Returns:
        Message: An instance of an email analyzer object.

    Raises:
        NotImplementedError: If the method is not implemented.
    """
    raise NotImplementedError
