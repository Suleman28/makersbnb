# This is an example of how to use the DatabaseConnection class
from lib.user import User
"""
When I seed the database
I get some records back
"""
def test_database_connection(db_connection):
    # Seed the database with some test data
    db_connection.seed("seeds/test_seed.sql")

    user = User("John Doe", "jd@email.com", "12345678")

    # Insert a new record
    db_connection.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', [
                                 user.name, user.email, user.password])

    # Retrieve all records
    result = db_connection.execute("SELECT * FROM users")

    # Assert that the results are what we expect
    assert result == [
        {
            'email': 'pp@email.com',
            'id': 1,
            'name': 'first_record',
            'name': 'Peter Puffin',
            'password': '12345678',
        },
        {
            'email': 'pollyp@email.com',
            'id': 2,
            'name': 'second_record',
            'name': 'Polly Penguin',
            'password': '12345678',
        },
        {
            'email': 'qq@email.com',
            'id': 3,
            'name': 'Quentin Quail',
            'password': '12345678',
        },
        {
            'email': 'jd@email.com',
            'id': 4,
            'name': 'John Doe',
            'password': '12345678',
        }
    ]
