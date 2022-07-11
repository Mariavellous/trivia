# requests module allows you to send HTTP requests. Install requests module.
import requests
import html
import random


# responsible for fetching trivia question info from API
class TriviaQuestion:
    def __init__(self):
        self.question = ""
        self.correct_answer = ""
        self.choices = []
        self.get_trivia_info()

    # Fetch trivia question from opentdb API
    def fetch_trivia(self):
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
        return question_data

    # Parse all necessary info from data
    def get_trivia_info(self):
        question_data = self.fetch_trivia()
        question_text = question_data["question"]
        self.question = html.unescape(question_text)
        answer = question_data["correct_answer"]
        self.correct_answer = html.unescape(answer)
        self.choices = question_data["incorrect_answers"]
        # Randomly add the correct answer to the list of incorrect answers to create list of choices
        integer = random.randint(0, 3)
        self.choices.insert(integer, self.correct_answer)







