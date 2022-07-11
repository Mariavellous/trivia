# requests module allows you to send HTTP requests. Install requests module.
import requests
import html
import random


parameters = {
    "amount": 1,
    # Category is Entertainment: Film
    "category": 11,
    "type": "multiple",
}

# make a get request to API endpoint including parameters
response = requests.get("https://opentdb.com/api.php", params=parameters)
# check any error status
response.raise_for_status()
# retrieve the data in json format
data = response.json()


# Retrieve a list of all questions
question_data = data["results"][0]
# print(question_data)

def get_trivia():
    question_text = question_data["question"]
    question = html.unescape(question_text)
    answer = question_data["correct_answer"]
    correct_answer = html.unescape(answer)
    choices = question_data["incorrect_answers"]
    # Randomnly add the correct answer to the list of incorrect answers to create list of choices
    integer = random.randint(0, 3)
    choices.insert(integer, correct_answer)
    return question, correct_answer, choices


# Parse all necessary info
# class Trivia:
#     def __init__(self, category, type, difficulty, question, correct_answer, incorrect_answer):
#         self.category = category
#         self.type = type
#         self.difficulty = difficulty
#         self.question = question
#         self.correct_answer = correct_answer
#         self.incorrect_answer = incorrect_answer



