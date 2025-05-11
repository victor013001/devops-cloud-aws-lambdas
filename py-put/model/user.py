class User:
    def __init__(self, id, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def from_dynamodb(cls, attributes):
        return cls(
            id=attributes["id"]["S"],
            name=attributes.get("name", {}).get("S"),
            email=attributes.get("email", {}).get("S"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
