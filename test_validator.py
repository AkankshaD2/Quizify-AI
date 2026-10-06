from quiz_generation.quiz_validator import validate_question
from quiz_generation.quiz_schema import QuizQuestion


# ============================================================
# SOURCE CHUNK
# ============================================================

chunk = {
    "topic": "5. LoRaWAN",
    "section": "Features",
    "content": (
        "Long Range "
        "Very Low Power "
        "Low Data Rate "
        "Wide Area Coverage "
        "Secure Communication "
        "High Scalability"
    )
}


# ============================================================
# TEST 1 — VALID QUESTION
# ============================================================

valid_question = QuizQuestion(
    question="What is a feature of LoRaWAN listed in the study notes?",

    options={
        "A": "Long Range",
        "B": "High Power",
        "C": "High Maintenance",
        "D": "Short Range"
    },

    correct_answer="A",

    explanation=(
        "Long Range is explicitly listed as a feature "
        "of LoRaWAN."
    ),

    difficulty="easy"
)


# ============================================================
# TEST 2 — HALLUCINATED ANSWER
# ============================================================

bad_answer_question = QuizQuestion(
    question="What is a feature of LoRaWAN listed in the study notes?",

    options={
        "A": "Automatic Routing",
        "B": "High Power",
        "C": "High Maintenance",
        "D": "Short Range"
    },

    correct_answer="A",

    explanation=(
        "Automatic Routing is explicitly listed as a "
        "feature of LoRaWAN."
    ),

    difficulty="easy"
)


# ============================================================
# TEST 3 — HALLUCINATED EXPLANATION
# ============================================================

bad_explanation_question = QuizQuestion(
    question="What is a feature of LoRaWAN listed in the study notes?",

    options={
        "A": "Long Range",
        "B": "High Power",
        "C": "High Maintenance",
        "D": "Short Range"
    },

    correct_answer="A",

    explanation=(
        "Long Range allows LoRaWAN to connect devices "
        "across cities and provides reliable communication "
        "for smart cities."
    ),

    difficulty="easy"
)


# ============================================================
# RUN TEST
# ============================================================

print("\n")
print("=" * 60)
print("TEST 1 — VALID QUESTION")
print("=" * 60)

result = validate_question(
    valid_question,
    chunk
)

print("\nEXPECTED: True")
print("ACTUAL:", result)


print("\n")
print("=" * 60)
print("TEST 2 — HALLUCINATED ANSWER")
print("=" * 60)

result = validate_question(
    bad_answer_question,
    chunk
)

print("\nEXPECTED: False")
print("ACTUAL:", result)


print("\n")
print("=" * 60)
print("TEST 3 — HALLUCINATED EXPLANATION")
print("=" * 60)

result = validate_question(
    bad_explanation_question,
    chunk
)

print("\nEXPECTED: False")
print("ACTUAL:", result)
