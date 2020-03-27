from components.jobs.job import Job
from typing import List
from gui.main_window import MainWindow
from tkinter import Tk

class TextJob(Job):
    FONT         = 'calibri'
    FONT_SIZE    = 40
    TEXT_COLOR   = 'white'
    STROKE_COLOR = 'black'

    def __init__(
        self,
        days_to_run: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        main_window: Tk,
        x: int,
        y: int
    ):
        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute)
        self._mainWindow = main_window
        self._text       = None
        self._stroke     = []
        self._x          = x
        self._y          = y

    def _getStroke(self):
        if not len(self._stroke):
            font = (self.FONT, self.FONT_SIZE)
            self._stroke.append(self._mainWindow.canvas.create_text(self._x - 2, self._y, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y - 2, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x + 2, self._y, font=font, fill=self.STROKE_COLOR))
            self._stroke.append(self._mainWindow.canvas.create_text(self._x, self._y + 2, font=font, fill=self.STROKE_COLOR))

        return self._stroke

    def _getText(self):
        if not self._text:
            self._text = self._mainWindow.canvas.create_text(
                self._x,
                self._y,
                font=(self.FONT, self.FONT_SIZE),
                fill=self.TEXT_COLOR
            )

        return self._text

    def _setText(self, text: str) -> None:
        for stroke in self._getStroke():
            self._mainWindow.canvas.itemconfigure(stroke, text=text)

        self._mainWindow.canvas.itemconfigure(self._getText(), text=text)

    def _destroy(self) -> None:
        if self._text:
            self._mainWindow.canvas.delete(self._text)
            self._text = None

        for stroke in self._stroke:
            self._mainWindow.canvas.delete(stroke)

        self._stroke = []