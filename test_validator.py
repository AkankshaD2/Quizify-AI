from quiz_schema import QuizQuestion
from quiz_generation.quiz_validator import validate_question


chunk = """
Long Range Very Low Power Low Data Rate Wide Area Coverage
Secure Communication High Scalability
"""


question = QuizQuestion(
    question="What is the primary characteristic of wireless sensor networks?",

    options={
        "A": "High Data Rate",
        "B": "Low Power Consumption",
        "C": "Wide Area Coverage",
        "D": "High Scalability"
    },

    correct_answer="C",

    explanation="Wireless sensor networks are designed for wide area coverage.",

    difficulty="easy"
)


result = validate_question(
    question,
    chunk
)


print("Validation result:", result)
