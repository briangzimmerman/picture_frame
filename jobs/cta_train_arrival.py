import asyncio
import json
import tkinter as tk

from components.apis.cta_trains.cta_train_client import CtaTrainClient
from components.apis.cta_trains.arrival_request import ArrivalRequest
from components.jobs.text_job import TextJob
from gui.main_window import MainWindow
from datetime import datetime
from typing import List
from requests.exceptions import RequestException

class CtaTrainArrival(TextJob):
    JOB_REPEAT_INTERVAL = 60
    TIME_FORMAT         = '%Y-%m-%dT%H:%M:%S' # 2020-03-24T20:26:57

    def __init__(
        self,
        days_to_run: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        cta_train_api_key: str,
        stop_id: int
    ):
        self._mainWindow = MainWindow.get()
        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute, self._mainWindow, tk.NE, 25, 15)

        self._ctaTrainClient = CtaTrainClient(cta_train_api_key)
        self._stop_id        = stop_id

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            if not self._shouldRunAgain(self.JOB_REPEAT_INTERVAL):
                await asyncio.sleep(self.JOB_PING_INTERVAL)
                continue

            self._setText('Trains in ' + self._getArrivalsMinutes() + ' minutes')
            self._mainWindow.update()
            
            self._lastRun = datetime.now()

        self._destroy()
        self._mainWindow.update()

        self._isRunning = False

    def _getArrivalsMinutes(self) -> str:
        try:
            response = self._ctaTrainClient.execute(ArrivalRequest(self._stop_id, 2))
        except RequestException as e:
            return 'unknown'

        responseData = json.loads(response.content)

        if not responseData['ctatt']['eta'][0]:
            return 'unknown'

        now                   = datetime.now()
        firstTrainArrivesAt   = datetime.strptime(responseData['ctatt']['eta'][0]['arrT'], self.TIME_FORMAT)
        secondsTillFirstTrain = (firstTrainArrivesAt - now).total_seconds()
        minutesTillFirstTrain = round(secondsTillFirstTrain / 60)

        if not minutesTillFirstTrain:
            minutesTillFirstTrain = '<1'

        if not responseData['ctatt']['eta'][1] or not responseData['ctatt']['eta'][1]['arrT']:
            return str(minutesTillFirstTrain)

        secondTrainArrivesAt = datetime.strptime(responseData['ctatt']['eta'][1]['arrT'], self.TIME_FORMAT)
        secondsTillSecondTrain = (secondTrainArrivesAt - now).total_seconds()
        minutesTillSecondTrain = round(secondsTillSecondTrain / 60)

        return str(minutesTillFirstTrain) + ' & ' + str(minutesTillSecondTrain)