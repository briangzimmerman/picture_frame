import asyncio
import time

from components.jobs.job import JobInterface
from typing import List

class JobManager:
    SLEEP_INTERVAL = 10

    def __init__(self, jobs: List[JobInterface]):
        self._jobCollection = jobs

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._startJobs())

    async def _startJobs(self) -> None:
        if not len(self._jobCollection): return

        while True:
            for job in self._jobCollection:
                if job.shouldBeRunning() and not job.isRunning():
                    asyncio.ensure_future(job.start())

            await asyncio.sleep(self.SLEEP_INTERVAL)