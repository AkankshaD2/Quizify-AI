
from quiz_scoring.answer_checker import check_answer

print(check_answer("A", "A"))
print(check_answer("b", "A"))
print(check_answer(" A ", "A"))
print(check_answer(None, "A"))
