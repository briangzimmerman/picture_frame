from components.apis.ipstack.ip_stack_client import IpStackClient
from components.http.request import Request

class CheckRequest(Request):

    def __init__(self):
        super().__init__(IpStackClient.BASE_URL + '/check', 'get')