from lib.user import User
from lib.user_repository import UserRepository
from lib.database_connection import DatabaseConnection

def test_all_returns_all_users():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = UserRepository(connection)

    users = repo.all()

    assert users == [
        User("Peter Puffin", "pp@email.com", "12445778", 1),
        User("Polly Penguin", "pollyp@email.com", "12345678", 2),
        User("Quentin Quail", "qq@email.com", "12649670", 3),
        User("Spears Sparrow", "spears@email.com", "12242650", 4)
    ]

def test_find_returns_the_correct_user():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = UserRepository(connection)

    user_to_find = repo.find(1)

    assert user_to_find == User("Peter Puffin", "pp@email.com", "12445778", 1)

def test_create_new_user_adds_to_users():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = UserRepository(connection)

    new_user = User("Clive Crane",
                    "cc@email.com",
                    "29572154",
                    4)

    repo.create(new_user)

    users = repo.all()

    assert len(users) == 5

def test_delete_user_removes_entry_from_list():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = UserRepository(connection)

    repo.delete(1)

    users = repo.all()

    assert users == [
        User("Polly Penguin", "pollyp@email.com", "12345678", 2),
        User("Quentin Quail", "qq@email.com", "12649670", 3),
        User("Spears Sparrow", "spears@email.com", "12242650", 4)
    ]


