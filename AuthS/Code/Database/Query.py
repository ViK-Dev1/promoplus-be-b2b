# classe per istanziare una query di qualsiasi tipo verso il DB
class Query:
    def __init__(self, query: str, params: dict):
        self.query = query
        self.params = params