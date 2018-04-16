class Recipe():
    def __init__(self, queue_number=None, date_created=None, date_update=None, status=None, user_id=None):
        self.queue_number = queue_number
        self.date_created = date_created
        self.date_update = date_update
        self.status = status
        self.user_id = user_id

    def to_json(self):
        return self.__dict__
