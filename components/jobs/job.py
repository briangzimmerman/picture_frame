from abc import ABC, abstractmethod
from datetime import time, datetime

class Job(ABC):
    def __init__(
        self,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ):
        self._isRunning  = False
        self._isStopping = False
        self._startTime  = time(start_hour, start_minute)
        self._endTime    = time(end_hour, end_minute)

    @abstractmethod
    async def start(self) -> None:
        pass

    def isRunning(self) -> bool:
        return self._isRunning

    def shouldBeRunning(self) -> bool:
        now = time(datetime.now().hour, datetime.now().minute)

        return self._startTime <= now < self._endTime
