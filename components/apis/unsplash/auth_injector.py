from components.http.injector import Injector

class AuthInjector(Injector):

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def inject(self, request):
        request.addHeader('Authorization', 'Client-ID ' + self.apiKey)