
def check_answer(selected_answer, correct_answer):
    """Check whether the selected answer is correct."""

    if selected_answer is None:
        return False

    return (
        selected_answer.strip().upper()
        == correct_answer.strip().upper()
    )
