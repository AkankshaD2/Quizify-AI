
from database.db_manager import (
    get_question_count,
    get_question_by_id,
    get_questions_by_difficulty
)

print("Total saved questions:", get_question_count())

print("\nQuestion with ID 3:")
question = get_question_by_id(3)

if question:
    print(question["question"])

print("\nEasy questions:", len(get_questions_by_difficulty("easy")))
