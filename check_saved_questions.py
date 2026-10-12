
from database.db_manager import get_all_questions

questions = get_all_questions()

print(f"Total saved questions: {len(questions)}")

for question in questions:
    print(f"\nID: {question['id']}")
    print(f"Question: {question['question']}")
    print(f"Answer: {question['correct_answer']}")
    print(f"Difficulty: {question['difficulty']}")
