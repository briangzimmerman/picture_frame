from components.http.client import Client
from components.apis.openweather.auth_injector import AuthInjector

class OpenweatherClient(Client):
    BASE_URL = 'https://api.openweathermap.org/data/2.5'

    def __init__(self, api_key: str):
        super().__init__()
        self.addInjector(AuthInjector(api_key))