class User:
    def __init__(self, name, email, password, id =None):
        self.id = id
        self.name= name
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"The User's details: ({self.name}, {self.email})"
