import asyncio
import json
import time

from components.jobs.job import JobInterface
from components.apis.unsplash.unsplash_client import UnsplashClient
from components.apis.unsplash.random_request import RandomRequest

class ArtJob(JobInterface):
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

    async def start(self) -> None:
        self._isRunning = True

        while self.shouldBeRunning():
            response     = self._unsplashClient.execute(
                RandomRequest('art', True, 'portrait', 1)
            )
            responseData = json.loads(response.content)
            print(responseData[0]['urls']['full'])

            await asyncio.sleep(self.JOB_REPEAT_INTERVAL)

        self._isRunning = False