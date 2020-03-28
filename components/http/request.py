class Request:
    
    def __init__(self, url: str, verb: str):
        self.params  = {}
        self.verb    = verb
        self.headers = {}
        self.json    = None
        self.url     = url

    def addHeader(self, key: str, value: str) -> 'Request':
        self.headers[key] = value

        return self

    def hasHeader(self, key: str) -> bool:
        return key in self.headers