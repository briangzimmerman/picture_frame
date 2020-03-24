from components.http.injector import Injector
from components.http.request import Request

class AuthInjector(Injector):

    def __init__(self, api_key: str):
        self._api_key = api_key

    def inject(self, request: Request) -> None:
        if 'key' not in request.params:
            request.params['key'] = self._api_key