import message

from . import _impl

# Dependency Injection of this implementation into the API
message.Message = _impl.GmailMessage