import inbox_client_api

from . import _impl

# Dependency Injection of this implementation into the API
#
inbox_client_api.get_client = lambda: _impl.Client()