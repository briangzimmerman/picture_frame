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
    JOB_REPEAT_INTERVAL = 3600 # 1 hour
    COLLECTIONS         = ['9387510', '9555007', '1336169', '5057079']

    def __init__(
        self,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int,
        unplash_api_key: str
    ):
        super().__init__(start_hour, start_minute, end_hour, end_minute)
        self._unsplashClient  = UnsplashClient(unplash_api_key)
        self._mainWindow      = MainWindow.get()
        self._photoImage      = None
        self._backgroundImage = None

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            self._setImage(self._getPhoto(self._getArtUrl()))
            self._mainWindow.update()
            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._destroyLabel()

        self._isRunning = False

    # TODO handle error
    def _getArtUrl(self) -> str:
        # TODO remove
        return 'https://cdn.mos.cms.futurecdn.net/jbCNvTM4gwr2qV8X8fW3ZB.png'
        
        # response     = self._unsplashClient.execute(RandomRequest(False, 'landscape', 1, collections=self.COLLECTIONS))
        # responseData = json.loads(response.content)

        # return responseData[0]['urls']['regular']

    def _getPhoto(self, photo_url: str) -> ImageTk.PhotoImage:
        img_bytes = urlopen(photo_url).read()
        image     = Image.open(BytesIO(img_bytes))
        image     = ImageOps.fit(
            image,
            (self._mainWindow.winfo_screenwidth(), self._mainWindow.winfo_screenheight())
        )

        return ImageTk.PhotoImage(image)

    def _destroyLabel(self) -> None:
        if self._backgroundImage:
            self._mainWindow.canvas.delete(self._backgroundImage)
            self._backgroundImage = None
            self._photoImage      = None

    def _setImage(self, bg_img: ImageTk.PhotoImage) -> None:
        if not self._backgroundImage:
            self._backgroundImage = self._mainWindow.canvas.create_image(0, 0, anchor=tk.NW, image=bg_img)
        else:
            self._mainWindow.canvas.itemconfigure(self._backgroundImage, image=bg_img)
            self._mainWindow.canvas.tag_lower(self._backgroundImage)

        self._photoImage = bg_img # keep image from being garbage collected
        