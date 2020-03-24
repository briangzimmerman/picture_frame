from components.http.injector import Injector
from components.http.request import Request

class OutputTypeInjector(Injector):

    def __init__(self, output_type: str):
        self._output_type = output_type

    def inject(self, request: Request) -> None:
        if 'outputType' not in request.params:
            request.params['outputType'] = self._output_type