from components.http.request import Request
from components.apis.unsplash.unsplash_client import UnsplashClient

class RandomRequest(Request):

    def __init__(self, featured: bool, orientation: str, count: int, query: str=None, collections: list=None):
        super().__init__(UnsplashClient.BASE_URL + '/photos/random', 'get')
        self.params = {
            "query": query,
            "featured": featured,
            "orientation": orientation,
            "count": count,
            "collections": ','.join(collections)
        }