from document_processing.vector_store import load_embeddings
from document_processing.retriever import search_chunks
from quiz_generation.question_generator import generate_question


# Load embeddings
chunks = load_embeddings("embeddings.pkl")


queries = [
    "Which protocol is designed for long-range communication with low power consumption?",
    "Which protocol uses the publish-subscribe model?",
    "Which protocol uses 128-bit addresses?"
]


for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    results = search_chunks(
        query,
        chunks,
        top_k=1
    )

    chunk = results[0]

    print("\nRetrieved Chunk:")
    print("Topic:", chunk["topic"])
    print("Section:", chunk["section"])
    print("Content:", chunk["content"])

    question = generate_question(
        chunk["content"]
    )

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
