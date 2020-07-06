class Counter():
    def __init__(self, date=None, count=None):
        self.date = date 
        self.count = str(count)

    def to_json(self):
        return self.__dict__
