from components.http.request import Request
from components.apis.unsplash.unsplash_client import UnsplashClient

class RandomRequest(Request):

    def __init__(self, query, featured, orientation, count):
        super().__init__(UnsplashClient.BASE_URL + '/photos/random', 'get')
        self.params = {
            "query": query,
            "featured": featured,
            "orientation": orientation,
            "count": count
        }