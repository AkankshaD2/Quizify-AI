def calculate_score(correct_answers, total_questions):
    """Calculate the quiz score as a percentage."""

    if total_questions < 0 or correct_answers < 0:
        raise ValueError("Counts cannot be negative.")

    if correct_answers > total_questions:
        raise ValueError("Correct answers cannot exceed total questions.")

    if total_questions == 0:
        return 0.0

    percentage = (correct_answers / total_questions) * 100

    return round(percentage, 2)
