from components.jobs.job import Job
from typing import List, Tuple
from gui.main_window import MainWindow

import tkinter as tk

class TextJob(Job):
    FONT             = 'Roboto'
    FONT_SIZE        = 38
    TEXT_COLOR       = 'white'
    STROKE_COLOR     = 'black'
    STROKE_THICKNESS = 1

    def __init__(
        self,
        days_to_run: List[int],
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        main_window: tk.Tk,
        anchor: str,
        x_margin: int,
        y_margin: int
    ):
        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute)
        self._mainWindow = main_window
        self._text       = None
        self._stroke     = []
        self._anchor     = anchor
        self._xMargin    = x_margin
        self._yMargin    = y_margin

    def __getStroke(self):
        if not len(self._stroke):
            font = (self.FONT, self.FONT_SIZE)
            self._stroke.append(self._mainWindow.canvas.create_text(0, 0, font=font, fill=self.STROKE_COLOR, anchor=tk.NW))
            self._stroke.append(self._mainWindow.canvas.create_text(0, 0, font=font, fill=self.STROKE_COLOR, anchor=tk.NW))
            self._stroke.append(self._mainWindow.canvas.create_text(0, 0, font=font, fill=self.STROKE_COLOR, anchor=tk.NW))
            self._stroke.append(self._mainWindow.canvas.create_text(0, 0, font=font, fill=self.STROKE_COLOR, anchor=tk.NW))

        return self._stroke

    def __getText(self):
        if not self._text:
            self._text = self._mainWindow.canvas.create_text(
                0,
                0,
                font=(self.FONT, self.FONT_SIZE),
                fill=self.TEXT_COLOR,
                anchor=tk.NW
            )

        return self._text

    def _setText(self, text: str) -> None:
        for stroke in self.__getStroke():
            self._mainWindow.canvas.itemconfigure(stroke, text = text)

        self._mainWindow.canvas.itemconfigure(self.__getText(), text=text)

        self.__setTextPosition()

    def _destroy(self) -> None:
        if self._text:
            self._mainWindow.canvas.delete(self._text)
            self._text = None

        for stroke in self._stroke:
            self._mainWindow.canvas.delete(stroke)

        self._stroke = []

    def __getTextHeight(self) -> int:
        box = self._mainWindow.canvas.bbox(self.__getText())

        return box[3] - box[1]

    def __getTextWidth(self) -> int:
        box = self._mainWindow.canvas.bbox(self.__getText())

        return box[2] - box[0]
    
    def __setTextPosition(self) -> None:
        (x, y) = self.__getTextNWCoords()

        self._mainWindow.canvas.coords(self.__getText(), x, y)
        self._mainWindow.canvas.coords(self.__getStroke()[0], x - self.STROKE_THICKNESS, y)
        self._mainWindow.canvas.coords(self.__getStroke()[1], x, y - self.STROKE_THICKNESS)
        self._mainWindow.canvas.coords(self.__getStroke()[2], x + self.STROKE_THICKNESS, y)
        self._mainWindow.canvas.coords(self.__getStroke()[3], x, y + self.STROKE_THICKNESS)

    def __getTextNWCoords(self) -> Tuple[int]:
        if self._anchor == tk.NW:
            return (self._xMargin, self._yMargin)
        if self._anchor == tk.N:
            return (self._xMargin - (self.__getTextWidth() / 2), self._yMargin)
        if self._anchor == tk.NE:
            return (
                self._mainWindow.winfo_screenwidth() - self.__getTextWidth() - self._xMargin, 
                self._yMargin
            )
        if self._anchor == tk.E:
            return (
                self._mainWindow.winfo_screenwidth() - self._xMargin - self.__getTextWidth(),
                self._yMargin - (self.__getTextHeight() / 2)
            )
        if self._anchor == tk.SE:
            return (
                self._mainWindow.winfo_screenwidth() - self._xMargin - self.__getTextWidth(),
                self._mainWindow.winfo_screenheight() - self._yMargin - self.__getTextHeight()
            )
        if self._anchor == tk.S:
            return (
                self._xMargin - (self.__getTextWidth() / 2),
                self._mainWindow.winfo_screenheight() - self._yMargin
            )
        if self._anchor == tk.SW:
            return (
                self._xMargin,
                self._mainWindow.winfo_screenheight() - self._yMargin - self.__getTextHeight()
            )
        if self._anchor == tk.W:
            return (self._xMargin, self._yMargin - (self.__getTextHeight() / 2))
        if self._anchor == tk.CENTER:
            return (
                self._xMargin - (self.__getTextWidth() / 2),
                self._yMargin - (self.__getTextHeight() / 2)
            )
        
        return (0, 0)