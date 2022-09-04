from datetime import date
import html


from TriviaQuestion import TriviaQuestion
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import json
from flask_bootstrap import Bootstrap5


from sqlalchemy import CheckConstraint


app = Flask(__name__)
app.secret_key = 'a random string'
bootstrap = Bootstrap5(app)
# create database in sqlite for now
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config['ENV'] = 'development'

app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)



class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), db.CheckConstraint('first_name > 0'), nullable=False)
    last_name = db.Column(db.String(30), db.CheckConstraint('last_name > 0'), nullable=False)
    # email_address VARCHAR(50) UNIQUE NOT NULL CHECK(email_address LIKE '%@%.%'),
    email_address = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), db.CheckConstraint('password > 0'), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(7500), db.CheckConstraint('text > 0'), nullable=False)
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
    return new_trivia.id


# Responsible for showing the trivia questions to player
@app.route('/play')
@login_required
def get_question():
    error = None
    # if count of trivia is less than 3 keep going. Otherwise, say "come play again tomorrow"
    num_questions = Guess.query.filter(Guess.player_id == current_user.id, Guess.played_on == date.today()).count()
    if num_questions < 3:
        new_trivia_id = add_trivia()
        # return new_trivia_id
        print(new_trivia_id)
        return redirect(url_for("show_question", trivia_id=new_trivia_id))
    else:
        return redirect(url_for("goodbye"))

@app.route('/goodbye')
def goodbye():
    return render_template("goodbye.html")

# Render the main page template
@app.route('/')
def home():
    return render_template('index.html')



# Create WTForms for Trivia Question
class TriviaForm(FlaskForm):

    options = RadioField("Choice", choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], validators=[DataRequired()])
    # choices = RadioField("Choice", choices=[("A", "B", "C", "D")], validators=[DataRequired()])
    submit = SubmitField("Register", validators=[DataRequired()])

# responsible for showing the question to user
@app.route('/question/<int:trivia_id>', methods=["GET"])
@login_required
def show_question(trivia_id):
    # popcorn = player.points
    trivia_form = TriviaForm()
    # get the question for the day
    # trivia_id = add_trivia()
    trivia = Question.query.get(trivia_id)
    print(trivia.correct_answer)
    question = trivia.text
    options = json.loads(trivia.choices)
    popcorn = "10 points"
    trivia_form.options.choices[0] = options[0]
    trivia_form.options.choices[1] = options[1]
    trivia_form.options.choices[2] = options[2]
    trivia_form.options.choices[3] = options[3]
    return render_template("trivia.html", form=trivia_form, question=question, trivia_id=trivia_id, popcorn=popcorn)


# responsible for retrieving player's answer and comparing player_answer to correct_answer
@app.route('/question/<int:trivia_id>', methods=["POST"])
@login_required
def show_player_answer(trivia_id):
    trivia = Question.query.get(trivia_id)
    # retrieve player_answer from the form
    player_answer = request.form.get("options")
    # print(player_answer)
    # save player's answer to the Guess database
    new_guess = Guess()
    new_guess.player_id = current_user.id
    new_guess.question_id = trivia_id
    new_guess.player_answer = player_answer
    new_guess.played_on = date.today()
    error = None

    # Compare player's answer to the correct answer
    correct_answer = trivia.correct_answer
    if player_answer == trivia.correct_answer:
        new_guess.result = True
        db.session.add(new_guess)
        db.session.commit()
        # State Player gets the correct answer
        # TODO: Add popcorn to user's profile
        # popcorn_points = current points + 10
        print("Your answer is right.")
        # Add popcorn to user's profile
        popcorn = "Here are your popcorn points"
        return render_template("result.html", popcorn=popcorn, correct_answer=correct_answer)
    else:
        new_guess.result = False
        db.session.add(new_guess)
        db.session.commit()
        error = f"Sorry, {player_answer} is wrong."
        return render_template("result.html", error=error, correct_answer=correct_answer)


# Register and Login Users
# Register new users
@app.route('/register', methods=["GET", "POST"])
def register_player():
    register_form = RegisterForm()
    error = None
    if request.method == "GET":
        # register_form = RegisterForm()
        return render_template("register.html", form=register_form)
    else:
        # retrieves data from player's input
        email = request.form.get("email")
        # check if email address exist in database
        player = Player.query.filter(Player.email_address == email).first()
        # if email already exist, state error
        if player is not None:
            error = "That email address already exist."
            return render_template("register.html", form=register_form, error=error)

        # retrieve and save player's input in the database
        new_player = Player()
        new_player.first_name = request.form.get("first_name")
        new_player.last_name = request.form.get("last_name")
        new_player.email_address = request.form.get("email")
        password = request.form.get("password")
        # Generate a hash of the password
        new_player.password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("login_player"))

# Create WTForms for Login
class LoginForm(FlaskForm):
    email = EmailField("Email")
    password = PasswordField("Password")
    login = SubmitField("Login")

# Create WTForms for Register
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    register = SubmitField("Register", validators=[DataRequired()])



@login_manager.user_loader
def load_user(user_id):
    return Player.query.get(user_id)

# Player will login successfully if check_password_hash == True
@app.route('/login', methods=["GET", "POST"])
def login_player():
    login_form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=login_form)
    else:
        error = None
        # retrieves data from player's input
        email = request.form.get("email")
        password = request.form.get("password")
        player = Player.query.filter(Player.email_address == email).first()
        if player is None:
            error = "That email does not exist. Please try again."
            return render_template("login.html", form=login_form, error=error)
        elif check_password_hash(player.password, password):
            login_user(player)
            return redirect(url_for("get_question"))
        else:
            error = "Incorrect password. Please try again."
            return render_template("login.html", error=error, form=login_form)

# User Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))



# TODO: Able to add popcorn points components to database.

# TODO: add popcorn points if player answer the question correctly.





# def show_trivia('/trivia', methods=['POST']):
    # Fetch the question/answer from API.
    # Update the QUESTION TABLE
    # new_trivia = Question(text=question_data["question"], correct_answer=question_data["correct_answer"],
    #                       choices=question_data["incorrect_answer"])
    # db.session.add(new_trivia)
    # db.session.commit()

# RESTFUL API routes
# /about
# (/) def get_all_trivia (past trivia's)
# /trivia
# /trivia/<int:id>
# /trivia/<int:id>/player_answer
# /trivia/<int:id>/correct_answer



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)



