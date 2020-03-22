from components.jobs.job import JobInterface
from components.apis.unsplash.unsplash_client import UnsplashClient

class ArtJob(JobInterface):

    def __init__(self, unplash_api_key: str):
        self.unsplashClient = UnsplashClient(unplash_api_key)

    def start(self) -> None:
        return

    def stop(self) -> None:
        return