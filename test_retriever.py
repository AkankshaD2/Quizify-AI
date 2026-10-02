from document_processing.vector_store import load_embeddings

from document_processing.retriever import (
    search_chunks,
    detect_requested_section,
    detect_requested_topic
)


# Load saved chunks + embeddings
chunks = load_embeddings("embeddings.pkl")

print("Loaded chunks:", len(chunks))


# Test topic + section queries
queries = [
    "What are the advantages of LoRaWAN?",
    "What are the limitations of MQTT?",
    "What are the features of IPv6?",
    "What is the definition of CoAP?"
]


for query in queries:

    print("\n")
    print("=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    # Detect requested section
    requested_section = detect_requested_section(query)

    # Detect requested topic
    requested_topic = detect_requested_topic(
        query,
        chunks
    )

    print("Detected section:", requested_section)
    print("Detected topic:", requested_topic)

    # Retrieve chunks
    results = search_chunks(
        query,
        chunks,
        top_k=5
    )

    print("\nRETRIEVED RESULTS:")

    for i, result in enumerate(
        results,
        start=1
    ):

        print("\nRESULT:", i)

        print(
            "Semantic similarity:",
            result["similarity"]
        )

        print(
            "Keyword score:",
            result["keyword_score"]
        )

        print(
            "Phrase score:",
            result["phrase_score"]
        )

        print(
            "Hybrid score:",
            result["hybrid_score"]
        )

        print(
            "Topic:",
            result["topic"]
        )

        print(
            "Section:",
            result["section"]
        )

        print(
            "Content:",
            result["content"]
        )

        print("-" * 70)
