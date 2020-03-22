import asyncio
import json
import time
import tkinter as tk

from components.jobs.job import Job
from components.apis.unsplash.unsplash_client import UnsplashClient
from components.apis.unsplash.random_request import RandomRequest
from components.utils.utils import get_fitted_image_dimensions
from gui.main_window import MainWindow
from urllib.request import urlopen
from PIL import Image, ImageTk, ImageOps
from io import BytesIO

class ArtJob(Job):
    JOB_REPEAT_INTERVAL = 3600

    def __init__(
        self,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        unplash_api_key: str
    ):
        super().__init__(start_hour, start_minute, end_hour, end_minute)
        self._unsplashClient = UnsplashClient(unplash_api_key)
        self._mainWindow     = MainWindow.get()

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            artUrl = self._getArtUrl()

            backgroundImage = self._getPhoto(artUrl)
            backgroundLabel = tk.Label(self._mainWindow, image=backgroundImage)
            backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
            backgroundLabel.pack()

            self._mainWindow.update()

            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._isRunning = False

    # TODO handle error
    def _getArtUrl(self) -> str:
        response     = self._unsplashClient.execute(RandomRequest('art', True, 'portrait', 1))
        responseData = json.loads(response.content)

        return responseData[0]['urls']['full']

    def _getPhoto(self, photo_url: str) -> ImageTk.PhotoImage:
        img_bytes = urlopen(photo_url).read()
        image     = Image.open(BytesIO(img_bytes))
        image     = ImageOps.fit(
            image,
            get_fitted_image_dimensions(
                image.size[0],
                image.size[1],
                self._mainWindow.winfo_screenwidth(),
                self._mainWindow.winfo_screenheight()
            )
        )

        return ImageTk.PhotoImage(image)