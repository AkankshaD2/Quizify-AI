
from quiz_generation.question_generator import generate_question
from database.db_manager import create_tables, save_question


def generate_quiz(chunks, max_retries=3):
    """
    Generate validated quiz questions,
    save them to SQLite, and return them.
    """

    create_tables()

    questions = []

    for chunk in chunks:

        for attempt in range(1, max_retries + 1):

            try:

                question = generate_question(chunk)

                # Save the validated question to SQLite
                question_id = save_question(question)

                print(
                    f"Question saved with ID: {question_id}"
                )

                questions.append(question)

                break

            except ValueError as error:

                print(f"\nAttempt {attempt} failed:")
                print(error)

                if attempt == max_retries:
                    raise ValueError(
                        "Failed to generate a valid "
                        "question after "
                        f"{max_retries} attempts."
                    )

    return questions
