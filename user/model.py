class User():
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def to_json(self):
        return self.__dict__
