import requests
import copy

class Client:

    def __init__(self):
        self.injectors = []

    def addInjector(self, injector):
        self.injectors.append(injector)

    def execute(self, request):
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