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
        User("Peter Puffin", "pp@email.com", "scrypt:32768:8:1$NS42sOePszYHDQW6$9872c8fd9fa3e41bb99f8ad55420e66a2c8f25c6e3ea5cf7b82c51a3e4dc0ae6cbbf145fe64446d619ac33dc2a69685958d8aef19b3912904bcc2732d4dc9693", 1),
        User("Polly Penguin", "pollyp@email.com", "scrypt:32768:8:1$d6MNCa3Rq5xTJoVN$f96b93f3289a8b2543ba7c3c778905d6b94f87f2e035f5b2fbb9a47aebccbcd4836afb47f7952dd33b3c7c8633816034398e25cf5255a4f1eaea5015ec2e51b8", 2),
        User("Quentin Quail", "qq@email.com", "scrypt:32768:8:1$SpSc2sKn7y7QM7Pd$aeb4f32ae6317a4fb1d1c0eaefe075f6a2334fd681b0c4b4cecfe5f890e78884c7bae7d4eb31f2e7542d83a5b51d767b1361f6caf1838b0671b70444731d853e", 3),
        User("Spears Sparrow", "spears@email.com", "scrypt:32768:8:1$lhO1WyJN97O7zdnm$ff0dfcb13b8890460bba985cff78e32696cc8c28995289a371d0cde7f58ef1cabd98a868eb269984da651f6f8122580b9869001a771b74651285f5669e7a08d1", 4)
    ]

def test_find_returns_the_correct_user():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = UserRepository(connection)

    user_to_find = repo.find(1)

    assert user_to_find ==  User("Peter Puffin", "pp@email.com", "scrypt:32768:8:1$NS42sOePszYHDQW6$9872c8fd9fa3e41bb99f8ad55420e66a2c8f25c6e3ea5cf7b82c51a3e4dc0ae6cbbf145fe64446d619ac33dc2a69685958d8aef19b3912904bcc2732d4dc9693", 1)
           

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
        User("Polly Penguin", "pollyp@email.com", "scrypt:32768:8:1$d6MNCa3Rq5xTJoVN$f96b93f3289a8b2543ba7c3c778905d6b94f87f2e035f5b2fbb9a47aebccbcd4836afb47f7952dd33b3c7c8633816034398e25cf5255a4f1eaea5015ec2e51b8", 2),
        User("Quentin Quail", "qq@email.com", "scrypt:32768:8:1$SpSc2sKn7y7QM7Pd$aeb4f32ae6317a4fb1d1c0eaefe075f6a2334fd681b0c4b4cecfe5f890e78884c7bae7d4eb31f2e7542d83a5b51d767b1361f6caf1838b0671b70444731d853e", 3),
        User("Spears Sparrow", "spears@email.com", "scrypt:32768:8:1$lhO1WyJN97O7zdnm$ff0dfcb13b8890460bba985cff78e32696cc8c28995289a371d0cde7f58ef1cabd98a868eb269984da651f6f8122580b9869001a771b74651285f5669e7a08d1", 4)
    ]


