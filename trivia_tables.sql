
CREATE TABLE IF NOT EXISTS player(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(30) NOT NULL CHECK (length (first_name) > 0),
    last_name VARCHAR(30) NOT NULL CHECK (length (last_name) > 0),
    email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    password VARCHAR NOT NULL CHECK(length(password) > 6)
);

CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text VARCHAR(200) NOT NULL (length(question) > 0),
    choices VARCHAR(200) NOT NULL (length (player_answer) > 0),
    correct_answer VARCHAR(100) NOT NULL (length (question) > 0),

);

CREATE TABLE IF NOT EXISTS guess(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    player_answer VARCHAR(100) NOT NULL (length (player_answer) > 0),
    played_on timestamp,
--     defaults to "False"
    result BOOLEAN DEFAULT NULL,
    CONSTRAINT player_id_fk FOREIGN KEY (player_id) REFERENCES player(id)
    CONSTRAINT question_id_fk FOREIGN KEY (question_id) REFERENCES question(id)
);

