class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

    @staticmethod
    def normalize_email(value):
        raise NotImplementedError

    @classmethod
    def from_mapping(cls, payload):
        raise NotImplementedError
