
CREATE TABLE IF NOT EXISTS players(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(30) NOT NULL CHECK (length (first_name) > 0),
    last_name VARCHAR(30) NOT NULL CHECK (length (last_name) > 0),
    email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    password VARCHAR NOT NULL CHECK(length(password) > 6)
);

CREATE TABLE IF NOT EXISTS trivia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    question VARCHAR(30) NOT NULL (length(question) > 0),
    correct_answer VARCHAR(30) NOT NULL (length (question) > 0),
    incorret_answer SET() NOT NULL,
    player_answer VARCHAR(30) NOT NULL (length (player_answer) > 0),
    played_on timestamp,
    result BOOLEAN DEFAULT NULL,
    CONSTRAINT player_id FOREIGN KEY (player_id) REFERENCES players(id)
);

