import html

import data
from data import question_data
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from data import *

app = Flask(__name__)
# create database in sqlite for now
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), db.CheckConstraint('first_name > 0'), nullable=False)
    last_name = db.Column(db.String(30), db.CheckConstraint('last_name > 0'), nullable=False)
    # email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    email_address = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), db.CheckConstraint('password > 0'), unique=True, nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), db.CheckConstraint('text > 0'), nullable=False)
    correct_answer = db.Column(db.String(100), db.CheckConstraint('correct_answer > 0'), nullable=False)
    # this is a string of data object
    choices = db.Column(db.String(100), db.CheckConstraint('choices > 0'), nullable=False)


class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(Player.id), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id), nullable=False)
    player_answer = db.Column(db.String(100), db.CheckConstraint('player_answer > 0'), nullable=False)
    played_on = db.Column(db.Date)
    result = db.Column(db.Boolean, nullable=False)


db.create_all()
db.session.commit()

# TODO: what are my REST API request.
# TODO: Make a get request to access trivia question for trivia API


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

def get_trivia_question:
    question = data.question_data()
    return question





# Render the main template
@app.route('/')
def home():
    return render_template('index.html')

def show_trivia('/trivia', methods=['GET']):
    pass


# TODO: Connect to heroku.


if __name__ == "__main__":
    main()



