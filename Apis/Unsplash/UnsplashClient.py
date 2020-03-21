from .Http import Client
import AuthInjector

class UnsplashClient(Client):
    BASE_URL = 'https://api.unsplash.com'

    def __init__(self, apiKey):
        super().__init__()
        self.addInjector(AuthInjector(apiKey))