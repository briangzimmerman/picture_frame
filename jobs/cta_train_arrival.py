import asyncio
import json
import tkinter as tk

from components.jobs.job import Job
from components.apis.cta_trains.cta_train_client import CtaTrainClient
from components.apis.cta_trains.arrival_request import ArrivalRequest
from gui.main_window import MainWindow
from datetime import datetime
from typing import List

class CtaTrainArrival(Job):
    JOB_REPEAT_INTERVAL = 60
    STROKE_COLOR        = 'black'
    TEXT_COLOR          = 'white'
    FONT                = 'calibri'
    FONT_SIZE           = 40
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
        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute)
        self._ctaTrainClient = CtaTrainClient(cta_train_api_key)
        self._mainWindow     = MainWindow.get()
        self._stop_id        = stop_id
        self._text           = None
        self._stroke         = []
        self._x              = self._mainWindow.winfo_screenwidth() - 275
        self._y              = 40

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            self._setText('Trains in ' + self._getArrivalsMinutes() + ' minutes')
            
            self._mainWindow.update()

            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._destroy()

        self._isRunning = False

    def _getArrivalsMinutes(self) -> str:
        response     = self._ctaTrainClient.execute(ArrivalRequest(self._stop_id, 2))
        responseData = json.loads(response.content)

        firstTrainArrivesAt  = datetime.strptime(responseData['ctatt']['eta'][0]['arrT'], self.TIME_FORMAT)
        secondTrainArrivesAt = datetime.strptime(responseData['ctatt']['eta'][1]['arrT'], self.TIME_FORMAT)

        now                    = datetime.now()
        secondsTillFirstTrain  = (firstTrainArrivesAt - now).total_seconds()
        secondsTillSecondTrain = (secondTrainArrivesAt - now).total_seconds()

        minutesTillFirstTrain = round(secondsTillFirstTrain / 60)
        if not minutesTillFirstTrain: minutesTillFirstTrain = '<1'

        minutesTillSecondTrain = round(secondsTillSecondTrain / 60)

        return str(minutesTillFirstTrain) + ' & ' + str(minutesTillSecondTrain)

    def _setText(self, text: str) -> None:
        for stroke in self._getStroke():
            self._mainWindow.canvas.itemconfigure(stroke, text=text)

        self._mainWindow.canvas.itemconfigure(self._getText(), text=text)

    def _getText(self):
        if not self._text:
            self._text = self._mainWindow.canvas.create_text(
                self._x,
                self._y,
                font=(self.FONT, self.FONT_SIZE),
                fill=self.TEXT_COLOR
            )

        return self._text

    def _getStroke(self):
        if not len(self._stroke):
            font = (self.FONT, self.FONT_SIZE)
            self._stroke.append(self._mainWindow.canvas.create_text(self._x - 2, self._y, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y - 2, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x + 2, self._y, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y + 2, font=font, fill=self.STROKE_COLOR))

        return self._stroke
    
    def _destroy(self) -> None:
        if self._text:
            self._mainWindow.canvas.delete(self._text)
            self._text = None

        for stroke in self._stroke:
            self._mainWindow.canvas.delete(stroke)

        self._stroke = []