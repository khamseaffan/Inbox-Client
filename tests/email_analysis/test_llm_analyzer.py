import pytest
from src.email_analysis_impl._impl import LLMAnalyzer


def test_analyze_spam_and_importance():
    analyzer = LLMAnalyzer()
    email = "Congratulations! You're a winner. Click here to claim your free prize."
    result = analyzer.analyze(email)

    assert result["spam"] is True
    assert result["importance"] == "normal"


def test_analyze_urgency():
    analyzer = LLMAnalyzer()
    email = "Please respond ASAP. This is urgent."
    result = analyzer.analyze(email)

    assert result["importance"] == "high"
    assert result["spam"] is False


def test_analyze_low_priority():
    analyzer = LLMAnalyzer()
    email = "Here is your weekly digest and newsletter update."
    result = analyzer.analyze(email)

    assert result["importance"] == "low"
    assert result["spam"] is False

def test_analyzer_detects_low_importance():
    analyzer = LLMAnalyzer()
    low_email = "You can ignore this message or mark it as low priority."
    result = analyzer.analyze(low_email)
    assert result["importance"] == "low"

@pytest.mark.parametrize("text,expected_spam,expected_importance", [
    ("Buy now and save!", True, "normal"),
    ("Hi, just checking in", False, "normal")
])
def test_parametrized_cases(text, expected_spam, expected_importance):
    analyzer = LLMAnalyzer()
    result = analyzer.analyze(text)
    assert result["spam"] == expected_spam
    assert result["importance"] == expected_importance
