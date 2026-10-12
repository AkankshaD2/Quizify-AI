from quiz_scoring.scoring_service import evaluate_quiz

user_answers = ["A", "B", "C", "A", "D"]
correct_answers = ["A", "C", "C", "B", "D"]

result = evaluate_quiz(user_answers, correct_answers)

print("Correct answers:", result["correct"])
print("Total questions:", result["total"])
print("Score:", result["percentage"], "%")
print("Answer results:", result["results"])
