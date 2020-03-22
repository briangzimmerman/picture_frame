from abc import ABC, abstractmethod
from components.http.request import Request

class Injector(ABC):

    @abstractmethod
    def inject(self, request: Request) -> None:
        pass