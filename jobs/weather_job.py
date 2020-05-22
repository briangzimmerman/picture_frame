from components.jobs.text_job import TextJob
from components.apis.openweather.openweather_client import OpenweatherClient
from components.apis.openweather.weather_request import WeatherRequest
from gui.main_window import MainWindow
from typing import List
from datetime import datetime

import json
import asyncio
import tkinter as tk

class WeatherJob(TextJob):
    JOB_REPEAT_INTERVAL = 1800

    def __init__(
        self,
        days_to_run: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        zip: str,
        openweather_api_key: str
    ):
        self._mainWindow = MainWindow.get()

        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute, self._mainWindow, tk.SW, 25, 25)

        self._openweatherClient = OpenweatherClient(openweather_api_key)
        self._zip               = zip

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            if not self._shouldRunAgain(self.JOB_REPEAT_INTERVAL):
                await asyncio.sleep(self.JOB_PING_INTERVAL)
                continue

            self._setText(str(self._getTemperature()) + '\u00b0')
            self._mainWindow.update()

            self._lastRun = datetime.now()

        self._destroy()
        self._mainWindow.update()

        self._isRunning = False
            

    def _getTemperature(self) -> int:
        response = self._openweatherClient.execute(WeatherRequest(self._zip))
        responseData = json.loads(response.content)

        return self._celciusToFahrenheit(responseData['main']['temp'])

    @staticmethod
    def _celciusToFahrenheit(celcius: str) -> int:
        return round((int(celcius) - 273.15) * 1.8 + 32)