import html
from data import question_data

def main():
    for question in question_data:
        question_q = question["question"]
        # decdde the HTML characters to its original character representation
        question_text = html.unescape(question_q)
        print(question_text)
        question_answer = question["correct_answer"]
        print(question_answer)
        incorrect_answers = question["incorrect_answers"]
        print(incorrect_answers)

# TODO: Create a database for the question.

if __name__ == "__main__":
    main()



