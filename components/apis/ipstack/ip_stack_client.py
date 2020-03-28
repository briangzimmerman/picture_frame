from components.http.client import Client
from components.apis.ipstack.auth_injector import AuthInjector

class IpStackClient(Client):
    BASE_URL = 'http://api.ipstack.com'

    def __init__(self, api_key: str):
        super().__init__()
        self.addInjector(AuthInjector(api_key))