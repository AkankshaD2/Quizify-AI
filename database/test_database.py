
from types import SimpleNamespace
from db_manager import create_tables, save_question, get_all_questions

create_tables()

sample_question = SimpleNamespace(
    question="Which protocol uses the publish-subscribe model?",
    options=SimpleNamespace(
        A="MQTT",
        B="IPv6",
        C="CoAP",
        D="Bluetooth"
    ),
    correct_answer="A",
    explanation="MQTT uses the publish-subscribe model.",
    difficulty="easy"
)

question_id = save_question(sample_question)
print("Saved question ID:", question_id)

questions = get_all_questions()

print("\nSaved questions:")

for question in questions:
    print("\nID:", question["id"])
    print("Question:", question["question"])
    print("Correct answer:", question["correct_answer"])
