from email_analysis_impl._impl import LLMAnalyzer

def test_analyze_spam():
    analyzer = LLMAnalyzer()
    result = analyzer.analyze("Click here to buy now!")
    assert result["spam"] is True
    assert result["importance"] == "normal"

def test_analyze_importance():
    analyzer = LLMAnalyzer()
    result = analyzer.analyze("Please respond ASAP to this issue.")
    assert result["spam"] is False
    assert result["importance"] == "high"
