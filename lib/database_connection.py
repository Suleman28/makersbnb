import os, psycopg
from dotenv import load_dotenv
from flask import g
from psycopg.rows import dict_row

load_dotenv()

class DatabaseConnection:
    def __init__(self, test_mode=False):
        self.connection = None
        self.test_mode = test_mode

    def _env_var_name(self):
        return "TEST_DATABASE_URL" if self.test_mode else "DATABASE_URL"

    # This method connects to PostgreSQL using the psycopg library, using the
    # connection string built from our environment variables (see connect_string.env).
    def connect(self):
        env_var = self._env_var_name()
        try:
            self.connection = psycopg.connect(
                self._connection_string(),
                row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database using {env_var}! " \
                    f"Did you set it in your .env file? See .example.env for the expected format.")

    # This method seeds the database with the given SQL file.
    # We use it to set up our database ready for our tests or application.
    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    # This method executes an SQL query on the database.
    # It allows you to set some parameters too. You'll learn about this later.
    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'

    # This private method checks that we're connected to the database.
    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    # This private method returns the connection string we should use, read
    # from the environment (see .example.env for the variables it expects).
    def _connection_string(self):
        env_var = self._env_var_name()
        connection_string = os.getenv(env_var)
        if not connection_string:
            raise Exception(f"{env_var} is not set! Copy .example.env to .env and fill it in.")

        # Guard against DATABASE_URL and TEST_DATABASE_URL being the same value:
        # seed() drops tables, so this protects the main database from being wiped
        # out by a test run.
        if self.test_mode and connection_string == os.getenv("DATABASE_URL"):
            raise Exception("TEST_DATABASE_URL must not be the same as DATABASE_URL!")

        return connection_string

# This function integrates with Flask to create one database connection that
# Flask request can use. To see how to use it, look at example_routes.py
def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = DatabaseConnection(
            test_mode=((os.getenv('APP_ENV') == 'test') or (app.config['TESTING'] == True))
        )
        g.flask_database_connection.connect()
    return g.flask_database_connection
