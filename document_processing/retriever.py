import re

import numpy as np
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


SECTION_NAMES = [
    "definition",
    "functions",
    "features",
    "advantages",
    "limitations"
]


STOP_WORDS = {
    "is", "are", "was", "were",
    "the", "a", "an",
    "of", "and", "with",
    "which", "what", "who",
    "how", "why", "when", "where",
    "used", "use", "for", "in", "to",
    "this", "that", "does", "do", "can"
}


IMPORTANT_PHRASES = [
    "long range",
    "low power",
    "wide area",
    "low data rate",
    "high scalability",
    "low maintenance",
    "large address space",
    "128 bit",
    "32 bit",
    "publish subscribe",
    "client server",
    "real time",
    "secure communication"
]


def normalize_text(text):
    """
    Normalize text for keyword and phrase comparison.
    """

    text = text.lower()

    # Convert hyphens to spaces
    text = text.replace("-", " ")

    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_keywords(text):
    """
    Extract meaningful individual words.
    """

    words = normalize_text(text).split()

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def calculate_keyword_score(query, text):
    """
    Calculate individual keyword overlap.

    Score = matching query keywords / total query keywords
    """

    query_words = get_keywords(query)
    text_words = get_keywords(text)

    if not query_words:
        return 0.0

    matching_words = query_words.intersection(text_words)

    return len(matching_words) / len(query_words)


def calculate_phrase_score(query, text):
    """
    Calculate important phrase overlap.

    Each matching phrase contributes to the score.
    """

    query_text = normalize_text(query)
    document_text = normalize_text(text)

    query_phrases = [
        phrase
        for phrase in IMPORTANT_PHRASES
        if phrase in query_text
    ]

    if not query_phrases:
        return 0.0

    matching_phrases = [
        phrase
        for phrase in query_phrases
        if phrase in document_text
    ]

    return len(matching_phrases) / len(query_phrases)


def detect_requested_section(query):
    """
    Detect whether the query asks for a specific section.
    """

    query_lower = query.lower()

    for section in SECTION_NAMES:

        if section in query_lower:
            return section.title()

    return None


def detect_requested_topic(query, chunks):
    """
    Detect the topic explicitly mentioned in the query.
    """

    query_lower = query.lower()

    for chunk in chunks:

        topic = chunk["topic"]

        # Example:
        # "5. LoRaWAN" -> "LoRaWAN"
        topic_name = topic.split(".", 1)[-1].strip()

        if topic_name.lower() in query_lower:
            return topic

    return None


def search_chunks(query, chunks, top_k=3):
    """
    Hybrid retrieval using:

    1. Semantic similarity
    2. Keyword overlap
    3. Important phrase matching
    4. Topic filtering
    5. Section filtering
    """

    # -----------------------------------------
    # STEP 1: Generate query embedding
    # -----------------------------------------

    query_embedding = model.encode([query])[0]

    # -----------------------------------------
    # STEP 2: Get chunk embeddings
    # -----------------------------------------

    chunk_embeddings = np.array(
        [chunk["embedding"] for chunk in chunks]
    )

    # -----------------------------------------
    # STEP 3: Calculate cosine similarity
    # -----------------------------------------

    similarities = np.dot(
        chunk_embeddings,
        query_embedding
    ) / (
        np.linalg.norm(chunk_embeddings, axis=1)
        * np.linalg.norm(query_embedding)
    )

    # -----------------------------------------
    # STEP 4: Detect topic and section
    # -----------------------------------------

    requested_section = detect_requested_section(query)

    requested_topic = detect_requested_topic(
        query,
        chunks
    )

    # -----------------------------------------
    # STEP 5: Calculate all scores
    # -----------------------------------------

    hybrid_scores = []

    for index, chunk in enumerate(chunks):

        semantic_score = float(
            similarities[index]
        )

        keyword_score = calculate_keyword_score(
            query,
            chunk["content"]
        )

        phrase_score = calculate_phrase_score(
            query,
            chunk["content"]
        )

        # Final hybrid score
        hybrid_score = (
            0.60 * semantic_score
            + 0.15 * keyword_score
            + 0.25 * phrase_score
        )

        hybrid_scores.append(
            hybrid_score
        )

    hybrid_scores = np.array(
        hybrid_scores
    )

    # -----------------------------------------
    # STEP 6: Filter by topic / section
    # -----------------------------------------

    if requested_topic and requested_section:

        matching_indices = [
            index
            for index, chunk in enumerate(chunks)
            if (
                chunk["topic"] == requested_topic
                and
                chunk["section"].lower()
                == requested_section.lower()
            )
        ]

    elif requested_topic:

        matching_indices = [
            index
            for index, chunk in enumerate(chunks)
            if chunk["topic"] == requested_topic
        ]

    else:

        matching_indices = list(
            range(len(chunks))
        )

    # -----------------------------------------
    # STEP 7: Rank results
    # -----------------------------------------

    ranked_indices = sorted(
        matching_indices,
        key=lambda index: hybrid_scores[index],
        reverse=True
    )[:top_k]

    # -----------------------------------------
    # STEP 8: Build results
    # -----------------------------------------

    results = []

    for index in ranked_indices:

        chunk = chunks[index]

        keyword_score = calculate_keyword_score(
            query,
            chunk["content"]
        )

        phrase_score = calculate_phrase_score(
            query,
            chunk["content"]
        )

        result = chunk.copy()

        result["similarity"] = float(
            similarities[index]
        )

        result["keyword_score"] = float(
            keyword_score
        )

        result["phrase_score"] = float(
            phrase_score
        )

        result["hybrid_score"] = float(
            hybrid_scores[index]
        )

        results.append(result)

    return results
