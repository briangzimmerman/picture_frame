from abc import ABC, abstractmethod
from datetime import time, datetime
from typing import List

class Job(ABC):
    def __init__(
        self,
        days_to_run: List[int], # 0 (Monday) though 6 (Sunday)
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ):
        self._isRunning   = False
        self._days_to_run = days_to_run
        self._startTime   = time(start_hour, start_minute)
        self._endTime     = time(end_hour, end_minute)

    @abstractmethod
    async def start(self) -> None:
        pass

    def isRunning(self) -> bool:
        return self._isRunning

    def shouldBeRunning(self) -> bool:
        if datetime.today().weekday() not in self._days_to_run: return False

        now = time(datetime.now().hour, datetime.now().minute)

        return self._startTime <= now < self._endTime
