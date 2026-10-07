from document_processing.vector_store import load_embeddings
from document_processing.retriever import search_chunks
from quiz_generation.quiz_service import generate_quiz


# Load embeddings
chunks = load_embeddings("embeddings.pkl")

retrieved_chunks = []

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

    retrieved_chunks.append(chunk)


print("\n" + "=" * 60)
print("GENERATING QUIZ FROM RETRIEVED CHUNKS")
print("=" * 60)


questions = generate_quiz(
    retrieved_chunks
)


for i, question in enumerate(questions, start=1):

    print(f"\nQuestion {i}:")
    print(question.question)

    print("\nOptions:")
    print("A:", question.options.A)
    print("B:", question.options.B)
    print("C:", question.options.C)
    print("D:", question.options.D)

    print("Correct Answer:", question.correct_answer)
    print("Explanation:", question.explanation)
    print("Difficulty:", question.difficulty)
