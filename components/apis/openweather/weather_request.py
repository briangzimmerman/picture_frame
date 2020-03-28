from components.http.request import Request
from components.apis.openweather.openweather_client import OpenweatherClient

class WeatherRequest(Request):

    def __init__(self, zip: str):
        super().__init__(OpenweatherClient.BASE_URL + '/weather', 'get')
        self.params = {
            'zip': zip
        }