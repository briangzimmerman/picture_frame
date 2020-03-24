from components.http.request import Request
from components.apis.cta_trains.cta_train_client import CtaTrainClient

class ArrivalRequest(Request):

    def __init__(self, stop_id: int):
        super().__init__(CtaTrainClient.BASE_URL + '/ttarrivals.aspx', 'get')
        self.params = {
            'stpid': stop_id
        }