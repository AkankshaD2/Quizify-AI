from quiz_generation.question_generator import generate_question


def generate_quiz(chunks, max_retries=3):
    """
    Generate one validated quiz question from each chunk.

    If a generated question fails validation,
    retry up to max_retries times.
    """

    questions = []

    for chunk in chunks:

        for attempt in range(1, max_retries + 1):

            try:

                question = generate_question(
                    chunk
                )

                questions.append(
                    question
                )

                break

            except ValueError as error:

                print(
                    f"\nAttempt {attempt} failed:"
                )

                print(
                    error
                )

                if attempt == max_retries:

                    raise ValueError(
                        "Failed to generate a valid "
                        "question after "
                        f"{max_retries} attempts."
                    )

    return questions
