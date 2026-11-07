
from quiz_generation.question_generator import generate_question


if __name__ == "__main__":

    chunk = {
        "unit": "FlowForge Mini Project",
        "topic": "Problem Statement",
        "section": "Introduction",
        "content": """
        Traditional 2D games generally use fixed enemy movement
        and fixed difficulty. Such games may not respond according
        to the way a player actually plays the game.

        A player may become stuck because the game does not provide
        useful guidance, while an experienced player may find the
        same challenge repetitive.

        The proposed project, FlowForge – AI Adaptive Dungeon,
        addresses this problem by developing a small interactive
        dungeon game in which basic Artificial Intelligence
        techniques are used for enemy navigation and player assistance.
        """
    }

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
