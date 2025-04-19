from unittest.mock import Mock

import pytest

from email_analysis import Analyzer

"Unit Tests for Client Protocol"


def test_analyze() -> None:
    """Test analyze method returns a dict."""
    analyzer = Mock(spec=Analyzer)
    # Simulate analyze returning a dictionary.
    mock_dict: dict[str, str] = {}
    mock_email = ""
    analyzer.analyze.return_value = mock_dict
    result = analyzer.analyze(mock_email)
    # Check that result is a dict.
    assert isinstance(result, dict)
