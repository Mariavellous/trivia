import html


from TriviaQuestion import TriviaQuestion
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy import CheckConstraint


app = Flask(__name__)
app.secret_key = 'a random string'

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


# Responsible for adding trivia question to the database
def add_trivia():
    trivia = TriviaQuestion()
    new_trivia = Question(text=trivia.question, correct_answer=trivia.correct_answer,
                          choices=json.dumps(trivia.choices))
    db.session.add(new_trivia)
    db.session.commit()


def main():
    add_trivia()




# Render the main templates
# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/')
def hello_melanie():
    return 'Hello, Melanie!'

# Register and Login Users


# Register new users
@app.route('/register', methods=["GET", "POST"])
def register_player():
    if request.method == "GET":
        register_form = RegisterForm()
        return render_template("register.html", form=register_form)


    else:
        # retrieves data from user_input
    #     new_player = request.json
        new_player = Player()
        new_player.first_name = request.form.get("first_name")
        new_player.last_name = request.form.get("last_name")
        new_player.email_address = request.form.get("email")
        password = request.form.get("password")
        # Generate a hash of the password
        new_player.password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
    #     player = Player(first_name=new_player['first_name'], last_name=new_player['last_name'],
    #                      email_address=new_player['email_address'],
    #                      password=password)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("login_player"))

# Create WTForms for Login
class LoginForm(FlaskForm):
    email = StringField("Email")
    password = StringField("Password")
    login = SubmitField("Login")

# Create WTForms for Register
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    register = SubmitField("Register", validators=[DataRequired()])



# Player will login successfully if check_password_hash = true
@app.route('/login', methods=["GET", "POST"])
def login_player():
    if request.method == "GET":
        login_form = LoginForm()
        return render_template("login.html", form=login_form)
    # else:
    #     # TODO: Need to retrieve data from user input using form
    #     #retrieves data from user input
    #     player = request.json
    #     email_address = player["email_address"]
    #     password = player["password"]

# TODO: Add user to database.
# TODO: Succesfully login a user.


# def show_trivia('/trivia', methods=['POST']):
    # Fetch the question/answer from API.
    # Update the QUESTION TABLE
    # new_trivia = Question(text=question_data["question"], correct_answer=question_data["correct_answer"],
    #                       choices=question_data["incorrect_answer"])
    # db.session.add(new_trivia)
    # db.session.commit()

# RESTFUL API routes
# /logout
# /login
# /register
# /about
# (/) def get_all_trivia (past trivia's)
# /trivia
# /trivia/<int:id>
# /trivia/<int:id>/player_answer
# /trivia/<int:id>/correct_answer


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)



