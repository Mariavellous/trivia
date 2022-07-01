# Brainstorm trivia project
from data import question_data


def main():
    for question in question_data:
        question_text = question["question"]
        print(question_text)
        question_answer = question["correct_answer"]
        print(question_answer)
        incorrect_answers = question["incorrect_answers"]
        print(incorrect_answers)


if __name__ == "__main__":
    main()



