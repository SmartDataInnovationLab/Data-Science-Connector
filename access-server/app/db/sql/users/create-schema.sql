--- name: create_schema#
CREATE TABLE IF NOT EXISTS users (
    token TEXT PRIMARY KEY,
    name TEXT NOT NULL
);