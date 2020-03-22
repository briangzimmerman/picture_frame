from components.http.request import Request
from components.http.injector import Injector

class AuthInjector(Injector):

    def __init__(self, apiKey: str):
        self.apiKey = apiKey

    def inject(self, request: Request) -> None:
        request.addHeader('Authorization', 'Client-ID ' + self.apiKey)