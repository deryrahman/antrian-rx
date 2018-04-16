class User():
    def __init__(self, name=None, email=None, role=None):
        self.name = name
        self.email = email
        self.role = role

    def to_json(self):
        return self.__dict__
