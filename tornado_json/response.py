class Paging(object):
    def __init__(self, limit, offset):


class Response(object):
    def __init__(self, data, paging):
        self.data = data
        self.paging = paging
