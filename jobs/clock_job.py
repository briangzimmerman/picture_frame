import asyncio
import tkinter as tk

from components.jobs.text_job import TextJob
from gui.main_window import MainWindow
from datetime import datetime
from typing import List

class ClockJob(TextJob):

    def __init__(self, days_to_run: List[int], start_hour: int, start_minute: int, end_hour: int, end_minute: int):
        self._mainWindow = MainWindow.get()
        x                = self._mainWindow.winfo_screenwidth() - 75
        y                = self._mainWindow.winfo_screenheight() - 30

        super().__init__(days_to_run, start_hour, start_minute, end_hour, end_minute, self._mainWindow, x, y)

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