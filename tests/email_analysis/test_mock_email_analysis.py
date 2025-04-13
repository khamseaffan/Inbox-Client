from email_analysis_impl.src.email_analysis_impl._impl import LLMAnalyzer

class MockLLMAnalyzer:
    """
    A mock version of LLMAnalyzer used for integration or pipeline tests.
    Always returns the same deterministic result.
    """
    def analyze(self, email_text: str) -> dict:
        return {
            "spam": False,
            "importance": "normal"
        }


def test_mock_analyzer_output():
    analyzer = MockLLMAnalyzer()
    result = analyzer.analyze("Any email text here.")

    assert result == {
        "spam": False,
        "importance": "normal"
    }
