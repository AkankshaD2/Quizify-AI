from quiz_generation.question_generator import generate_question
from database.db_manager import create_tables, save_question


def generate_quiz(chunks, question_count=10, max_retries=3):
    """
    Generate the requested number of validated quiz questions.
    """

    create_tables()

    questions = []

    if len(chunks) < question_count:
        raise ValueError(
            f"Not enough chunks. Found {len(chunks)} chunks, "
            f"but {question_count} questions were requested."
        )

    for chunk in chunks:

        if len(questions) >= question_count:
            break

        for attempt in range(1, max_retries + 1):

            try:
                question = generate_question(chunk)

                question_id = save_question(question)

                print(f"Question saved with ID: {question_id}")

                questions.append(question)

                break

            except ValueError as error:

                print(f"\nAttempt {attempt} failed:")
                print(error)

                if attempt == max_retries:
                    print("Skipping this chunk after failed retries.")

    if len(questions) < question_count:
        raise ValueError(
            f"Only {len(questions)} valid questions were generated. "
            f"{question_count} were requested."
        )

    return questions