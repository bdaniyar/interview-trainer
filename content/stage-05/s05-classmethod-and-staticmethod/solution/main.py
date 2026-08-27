class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

    @staticmethod
    def normalize_email(value):
        return value.strip().lower()

    @classmethod
    def from_mapping(cls, payload):
        user_id = payload["id"]
        email = cls.normalize_email(payload["email"])
        if user_id <= 0 or not email:
            raise ValueError("invalid user")
        return cls(user_id, email)
