import asyncio
import tkinter as tk

from components.jobs.job import Job
from gui.main_window import MainWindow
from datetime import datetime

class ClockJob(Job):
    STROKE_COLOR = 'black'
    TEXT_COLOR   = 'white'
    FONT         = 'calibri'
    FONT_SIZE    = 40

    def __init__(self, start_hour: int, start_minute: int, end_hour: int, end_minute: int):
        super().__init__(start_hour, start_minute, end_hour, end_minute)
        self._text       = None
        self._stroke     = []
        self._mainWindow = MainWindow.get()
        self._x          = self._mainWindow.winfo_screenwidth() - 75
        self._y          = self._mainWindow.winfo_screenheight() - 30

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            now  = datetime.now()
            time = now.strftime('%-I:%M')
            
            self._setText(time)

            self._mainWindow.update()

            await asyncio.sleep(1)

        self._destroy()

        self._isRunning = False

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
            self._stroke.append(self._mainWindow.canvas.create_text(self._x - 2, self._y, font=font,fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y - 2, font=font,fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x + 2, self._y, font=font,fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y + 2, font=font,fill=self.STROKE_COLOR))

        return self._stroke

    def _destroy(self) -> None:
        if self._text:
            self._mainWindow.canvas.delete(self._text)
            self._text = None

        for stroke in self._stroke:
            self._mainWindow.canvas.delete(stroke)

        self._stroke = []