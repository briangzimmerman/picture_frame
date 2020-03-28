from components.http.injector import Injector
from components.http.request import Request

class AuthInjector(Injector):

    def __init__(self, ipstack_api_key: str):
        self._ipstack_api_key = ipstack_api_key

    def inject(self, request: Request) -> None:
        if 'access_key' not in request.params:
            request.params['access_key'] = self._ipstack_api_key