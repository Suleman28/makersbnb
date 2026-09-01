from lib.user import User 

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all users
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["name"], row["email"], row["password"], row["password_confirmation"], row["id"])
            users.append(item)
        return users

    # Find a single user by their id
    def find(self, user_id):
        rows = self._connection.execute(
            'SELECT * from users WHERE id = %s', [user_id])
        row = rows[0]
        return User(row["name"], row["email"], row["password"], row["password_confirmation"], row["id"])

    # Create a new user
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, user):
        self._connection.execute('INSERT INTO users (name, email, password, password_confirmation) VALUES (%s, %s, %s, %s)', [
                                 user.name, user.email, user.password, user.password_confirmation])
        return None

    # Delete a user by their id
    def delete(self, user_id):
        self._connection.execute(
            'DELETE FROM users WHERE id = %s', [user_id])
        return None
