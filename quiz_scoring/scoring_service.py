from quiz_scoring.answer_checker import check_answer
from quiz_scoring.score_calculator import calculate_score


def evaluate_quiz(user_answers, correct_answers):
    """Evaluate quiz answers and return the score."""

    if len(user_answers) != len(correct_answers):
        raise ValueError("Answer lists must have the same length.")

    correct_count = 0
    results = []

    for user_answer, correct_answer in zip(
        user_answers, correct_answers
    ):
        is_correct = check_answer(user_answer, correct_answer)
        results.append(is_correct)

        if is_correct:
            correct_count += 1

    total_questions = len(correct_answers)
    percentage = calculate_score(correct_count, total_questions)

    return {
        "correct": correct_count,
        "total": total_questions,
        "percentage": percentage,
        "results": results,
    }
