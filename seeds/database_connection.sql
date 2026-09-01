-- Minimal seed file used by tests/test_database_connection.py
-- This only tests that DatabaseConnection can seed and query the test database.

DROP TABLE IF EXISTS test_table;

CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

INSERT INTO test_table (name) VALUES ('first_record');
