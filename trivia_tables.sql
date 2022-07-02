
CREATE TABLE IF NOT EXISTS players(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(30) NOT NULL CHECK (length (first_name) > 0),
    last_name VARCHAR(30) NOT NULL CHECK (length (last_name) > 0),
    email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    password VARCHAR NOT NULL CHECK(length(password) > 6)
);

