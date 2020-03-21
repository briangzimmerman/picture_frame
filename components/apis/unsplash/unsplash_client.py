from components.http.client import Client
from components.apis.unsplash.auth_injector import AuthInjector

class UnsplashClient(Client):
    BASE_URL = 'https://api.unsplash.com'

    def __init__(self, apiKey):
        super().__init__()
        self.addInjector(AuthInjector(apiKey))