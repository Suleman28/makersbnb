from lib.database_connection import DatabaseConnection

# Run this file to reset your development database using seeds/seed.sql
# ; python seed_database.py

connection = DatabaseConnection(test_mode=True)
connection.connect()
connection.seed("seeds/test_seed.sql")
