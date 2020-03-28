from components.jobs.text_job import TextJob
from components.apis.openweather.openweather_client import OpenweatherClient
from components.apis.openweather.weather_request import WeatherRequest
from components.apis.ipstack.ip_stack_client import IpStackClient
from components.apis.ipstack.check_request import CheckRequest
from gui.main_window import MainWindow
from typing import List

import json
import asyncio

class WeatherJob(TextJob):
    JOB_REPEAT_INTERVAL = 1800

    def __init__(
        self,
        days_to_run: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        ipstack_api_key: str,
        openweather_api_key: str
    ):
        self._mainWindow = MainWindow.get()
        x                = 60
        y                = self._mainWindow.winfo_screenheight() - 30

        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute, self._mainWindow, x, y)

        self._openweatherClient = OpenweatherClient(openweather_api_key)
        
        ipstack      = IpStackClient(ipstack_api_key)
        response     = ipstack.execute(CheckRequest())
        responseData = json.loads(response.content)

        self._zip = responseData['zip']

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            self._setText(str(self._getTemperature()) + '\u00b0')

            self._mainWindow.update()

            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._destroy()

        self._isRunning = False
            

    def _getTemperature(self) -> int:
        response = self._openweatherClient.execute(WeatherRequest(self._zip))
        responseData = json.loads(response.content)

        return self._celciusToFahrenheit(responseData['main']['temp'])

    @staticmethod
    def _celciusToFahrenheit(celcius: str) -> int:
        return round((int(celcius) - 273.15) * 1.8 + 32)