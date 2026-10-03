from ollama import chat

from quiz_schema import QuizQuestion
from quiz_generation.quiz_validator import validate_question


def generate_question(chunk):

    prompt = f"""
You are an educational quiz generator.

Generate ONE high-quality multiple-choice question from the study notes below.

STRICT RULES:

1. Generate exactly ONE question.
2. Generate exactly 4 options: A, B, C, D.
3. Only ONE option must be correct.
4. Keep all options short and clear.
5. Options should normally be a phrase, not a long sentence.
6. Make the incorrect options plausible but clearly incorrect based on the study notes.
7. Use ONLY the information explicitly present in the study notes.
8. The question must be about the SAME topic as the study notes.
9. Do NOT introduce related concepts, applications, technologies, or terms that are not explicitly mentioned in the study notes.
10. Every option must be answerable using only the study notes.
11. The correct answer must be directly supported by the study notes.
12. The explanation must use only information from the study notes.
13. The question must directly test a fact, relationship, or comparison stated in the study notes.
14. Do NOT create a question about the general field, technology category, or real-world application unless it is explicitly stated in the notes.
15. Do NOT invent numbers, quantities, device types, use cases, or comparisons.
16. Every option must use only terms or facts found in the study notes.
17. Do not add words such as "only", "trillions", "human devices", or similar qualifiers unless they appear in the study notes.
18. Prefer questions that directly use the terminology from the study notes.
19. Choose difficulty:
    - easy = direct recall of a fact explicitly stated in the notes
    - medium = combine two or more facts explicitly stated in the notes
    - hard = reasoning using facts explicitly stated in the notes
IMPORTANT:
The study notes are the ONLY source of truth.

Before generating the question:
1. Identify the main topic in the study notes.
2. Identify the exact facts available in the study notes.
3. Create the question using those facts only.
4. Create all four options using only those facts.
5. Check that exactly one option is supported as the answer.
6. Remove any option that contains information not present in the notes.

Do not use your general knowledge.
Do not infer missing information.
Do not introduce new examples, numbers, devices, applications, or comparisons.
Study notes:
{chunk}

Return EXACTLY this format:

QUESTION: <question>

A: <short option>
B: <short option>
C: <short option>
D: <short option>

ANSWER: <A/B/C/D>

EXPLANATION: <short explanation>

DIFFICULTY: <easy/medium/hard>
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = response.message.content

    lines = [
        line.strip()
        for line in raw_response.splitlines()
        if line.strip()
    ]

    question_text = ""
    options = {}
    correct_answer = ""
    explanation = ""
    difficulty = ""

    for line in lines:

        if line.startswith("QUESTION:"):
            question_text = line.replace(
                "QUESTION:", ""
            ).strip()

        elif line.startswith("A:"):
            options["A"] = line.replace(
                "A:", ""
            ).strip()

        elif line.startswith("B:"):
            options["B"] = line.replace(
                "B:", ""
            ).strip()

        elif line.startswith("C:"):
            options["C"] = line.replace(
                "C:", ""
            ).strip()

        elif line.startswith("D:"):
            options["D"] = line.replace(
                "D:", ""
            ).strip()

        elif line.startswith("ANSWER:"):
            correct_answer = line.replace(
                "ANSWER:", ""
            ).strip()

        elif line.startswith("EXPLANATION:"):
            explanation = line.replace(
                "EXPLANATION:", ""
            ).strip()

        elif line.startswith("DIFFICULTY:"):
            difficulty = line.replace(
                "DIFFICULTY:", ""
            ).strip()

    quiz_question = QuizQuestion(
        question=question_text,
        options=options,
        correct_answer=correct_answer,
        explanation=explanation,
        difficulty=difficulty
    )

    is_valid = validate_question(
        quiz_question,
        chunk
    )

    if not is_valid:
        raise ValueError(
            "Generated question failed grounding validation."
        )

    return quiz_question
