from lib.database_connection import DatabaseConnection

# Run this file to reset your development database using seeds/seed.sql
# ; python seed_database.py

connection = DatabaseConnection(test_mode=False)
connection.connect()
connection.seed("seeds/seed.sql")
