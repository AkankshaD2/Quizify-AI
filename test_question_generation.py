from quiz_generation.question_generator import generate_question


if __name__ == "__main__":

    chunk = """
    IPv6 is the latest Internet Protocol using
    128-bit addresses to support billions of IoT devices.
    """

    question = generate_question(chunk)

    print("\n===== GENERATED QUIZ =====")

    print("\nQuestion:")
    print(question.question)

    print("\nOptions:")
    print("A:", question.options.A)
    print("B:", question.options.B)
    print("C:", question.options.C)
    print("D:", question.options.D)

    print("\nCorrect Answer:", question.correct_answer)

    print("Explanation:", question.explanation)

    print("Difficulty:", question.difficulty)
