# requests module allows you to send HTTP requests. Install requests module.
import requests


parameters = {
    "amount": 3,
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
question_data = data["results"]
# print(question_data)

# Parse all necessary info from 0th index question.
# question = data["results"][0]["question"]
# print(question)
# correct_answer = data["results"][0]["correct_answer"]
# print(correct_answer)
# incorrect_answers = data["results"][0]["incorrect_answers"]
# print(incorrect_answers)




