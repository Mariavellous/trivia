
CREATE TABLE IF NOT EXISTS players(
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

    player_id INTEGER NOT NULL,
    player_answer VARCHAR(100) NOT NULL (length (player_answer) > 0),
    played_on timestamp,
    result BOOLEAN DEFAULT NULL,
    CONSTRAINT player_id FOREIGN KEY (player_id) REFERENCES players(id)


class Question(db.Model):
    choices = db.Column(db.String(100), db.CheckConstraint('choices > 0'), nullable=False)

