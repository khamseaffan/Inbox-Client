import email_analysis_api  # Correct package name for the API
from . import _impl


if hasattr(email_analysis_api, 'get_analyzer'):
    email_analysis_api.get_analyzer = _impl.get_analyzer
    print("DI: Injected _impl.get_analyzer into email_analysis_api.get_analyzer")
else:
    print("DI ERROR: email_analysis_api does NOT have get_analyzer attribute before DI assignment!")
