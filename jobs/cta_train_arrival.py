import asyncio
import json
import tkinter as tk

from components.jobs.job import Job
from components.apis.cta_trains.cta_train_client import CtaTrainClient
from components.apis.cta_trains.arrival_request import ArrivalRequest
from gui.main_window import MainWindow

class CtaTrainArrival(Job):
    JOB_REPEAT_INTERVAL = 60
    STROKE_COLOR        = 'black'
    TEXT_COLOR          = 'white'
    FONT                = 'calibri'
    FONT_SIZE           = 40

    def __init__(
        self,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        cta_train_api_key: str,
        stop_id: int
    ):
        super().__init__(start_hour, start_minute, end_hour, end_minute)
        self._ctaTrainClient = CtaTrainClient(cta_train_api_key)
        self._mainWindow     = MainWindow.get()
        self._stop_id        = stop_id
        self._text           = None
        self._stroke         = None
        self._x              = self._mainWindow.winfo_screenwidth() - 275
        self._y              = 40

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            arrives_in = self._getNextArrivalMinutes()
            text       = 'Next train in ' + str(arrives_in) + ' minute'

            if arrives_in > 1: text = text + 's'
            
            self._setText(text)
            self._mainWindow.update()

            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._destroy()

        self._isRunning = False

    def _getNextArrivalMinutes(self):
        # response     = self._ctaTrainClient.execute(ArrivalRequest(self._stop_id))
        # responseData = json.loads(response.content)

        return 5 #TODO make this work

    def _setText(self, text: str) -> None:
        self._mainWindow.canvas.itemconfigure(self._getStroke(), text=text)
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
        if not self._stroke:
            self._stroke = self._mainWindow.canvas.create_text(
                self._x,
                self._y,
                font=(self.FONT, self.FONT_SIZE, 'bold'),
                fill=self.STROKE_COLOR
            )

        return self._stroke
    
    def _destroy(self) -> None:
        if self._text:
            self._mainWindow.canvas.delete(self._text)
            self._text = None

        if self._stroke:
            self._mainWindow.canvas.delete(self._stroke)
            self._stroke = None