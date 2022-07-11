import html
from data import get_trivia
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import CheckConstraint

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
    text = db.Column(db.String(5000), db.CheckConstraint('text > 0'), nullable=False)
    correct_answer = db.Column(db.String(1000), db.CheckConstraint('correct_answer > 0'), nullable=False)
    # this is a string of data object
    choices = db.Column(db.String(1000), db.CheckConstraint('choices > 0'), nullable=False)


class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(Player.id), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id), nullable=False)
    player_answer = db.Column(db.String(1000), db.CheckConstraint('player_answer > 0'), nullable=False)
    played_on = db.Column(db.Date)
    result = db.Column(db.Boolean, nullable=False)


db.create_all()
db.session.commit()

# TODO: what are my REST API request.

(question, correct_answer, choices) = get_trivia()
new_trivia = Question(text=question, correct_answer=correct_answer,
                      choices=json.dumps(choices))
db.session.add(new_trivia)
db.session.commit()


# (question, correct_answer, choices) = trivia
# print(question)
# print(correct_answer)
# print(choices)


def main():
    get_trivia()




# Render the main template
# @app.route('/')
# def home():
#     return render_template('index.html')

# def show_trivia('/trivia', methods=['POST']):
    # Fetch the question/answer from API.
    # Update the QUESTION TABLE
    # new_trivia = Question(text=question_data["question"], correct_answer=question_data["correct_answer"],
    #                       choices=question_data["incorrect_answer"])
    # db.session.add(new_trivia)
    # db.session.commit()





# TODO: Connect to heroku.


if __name__ == "__main__":
    main()



