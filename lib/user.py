class User:
    SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~\\")

    def __init__(self, name, email, password, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"The User's details: ({self.name}, {self.email})"

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char in User.SPECIAL_CHARACTERS for char in password):
            raise ValueError("Password must contain at least one special character.")
