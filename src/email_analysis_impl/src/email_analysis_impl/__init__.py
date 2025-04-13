import email_analysis_api  # Correct package name for the API
from . import _impl


email_analysis_api.get_analyzer = _impl.get_analyzer
    