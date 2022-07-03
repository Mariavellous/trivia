import html
from data import question_data
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

app = Flask(__name__)
# create database in sqlite for now
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia-collection.db'

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), db.CheckConstraint('first_name > 0'), nullable=False)
    last_name = db.Column(db.String(30), db.CheckConstraint('last_name > 0'), nullable=False)
    # email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    email_address = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), db.CheckConstraint('password > 0'), unique=True, nullable=False)


class Trivia(db.Modle):
    id = db.Column(db.Integer, primary_key=True)
    # foreign key
    # CONSTRAINT player_id FOREIGN KEY (player_id) REFERENCES players(id)
    player_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(30), db.CheckConstraint('question > 0'), nullable=False)
    correct_answer = db.Column(db.String(30), db.CheckConstraint('correct_answer > 0'), nullable=False)
    # this needs to be a set
    # incorret_answer SET() NOT NULL,
    incorrect_answers = db.Column(db.String(30), db.CheckConstraint('correct_answer > 0'), nullable=False)
    player_answer = db.Column(db.String(30), db.CheckConstraint('player_answer > 0'), nullable=False)
    # timestamp
    # played_on = db.Column(, nullable=False
    # boolean
    result = db.Column()
    # result BOOLEAN DEFAULT NULL,

def main():
    for question in question_data:
        question_q = question["question"]
        # decode the HTML characters to its original character representation
        question_text = html.unescape(question_q)
        print(question_text)
        question_answer = question["correct_answer"]
        print(question_answer)
        incorrect_answers = question["incorrect_answers"]
        print(incorrect_answers)

# TODO: Create a database for the question. What other tables do I need? 


if __name__ == "__main__":
    main()



