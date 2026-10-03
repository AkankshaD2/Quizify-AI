from quiz_schema import QuizQuestion


question = QuizQuestion(
    question="Which protocol uses 128-bit addresses?",

    options={
        "A": "IPv4",
        "B": "IPv6",
        "C": "MQTT",
        "D": "CoAP"
    },

    correct_answer="B",

    explanation="IPv6 uses 128-bit addresses.",

    difficulty="easy"
)


print(question)
print("\nOptions:")
print("A:", question.options.A)
print("B:", question.options.B)
print("C:", question.options.C)
print("D:", question.options.D)
