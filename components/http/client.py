import requests
import copy

from components.http.injector import Injector
from components.http.request import Request

class Client:

    def __init__(self):
        self.injectors = []

    def addInjector(self, injector: Injector) -> None:
        self.injectors.append(injector)

    def execute(self, request: Request) -> requests.Response:
        requestCopy = copy.deepcopy(request)

        for injector in self.injectors:
            injector.inject(requestCopy)

        return requests.request(
            requestCopy.verb,
            requestCopy.url,
            params=requestCopy.params,
            json=requestCopy.json,
            headers=requestCopy.headers
        )