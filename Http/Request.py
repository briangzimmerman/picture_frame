class Request:
    
    def __init__(self, url, verb):
        self.params  = None
        self.verb    = verb
        self.headers = {}
        self.json    = None
        self.url     = url

    def addHeader(self, key, value):
        self.headers[key] = value;

        return self