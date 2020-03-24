from components.http.client import Client
from components.apis.cta_trains.auth_injector import AuthInjector
from components.apis.cta_trains.output_type_injector import OutputTypeInjector

class CtaTrainClient(Client):
    BASE_URL = 'http://lapi.transitchicago.com/api/1.0'

    def __init__(self, api_key: str):
        super().__init__()
        self.addInjector(AuthInjector(api_key))
        self.addInjector(OutputTypeInjector('JSON'))