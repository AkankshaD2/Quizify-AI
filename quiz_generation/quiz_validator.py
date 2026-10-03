import re


def normalize_text(text):
    """
    Normalize text for simple fact checking.
    """

    text = text.lower()

    text = text.replace("-", " ")

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def validate_question(question, chunk):
    """
    Basic validation to check whether the generated
    question stays grounded in the retrieved chunk.
    """

    source_text = normalize_text(chunk)

    question_text = normalize_text(
        question.question
    )

    explanation_text = normalize_text(
        question.explanation
    )

    # Combine question + explanation
    generated_text = (
        question_text
        + " "
        + explanation_text
    )

    # Extract important words from source
    source_words = set(source_text.split())

    # Extract generated words
    generated_words = set(
        generated_text.split()
    )

    # Words introduced by the LLM
    new_words = generated_words - source_words

    # Ignore common English words
    ignored_words = {
        "what",
        "which",
        "is",
        "are",
        "the",
        "a",
        "an",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "does",
        "do",
        "used",
        "use",
        "uses",
        "main",
        "primary",
        "key",
        "characteristic",
        "according",
        "study",
        "notes",
        "state",
        "states",
        "described",
        "description"
    }

    new_words = new_words - ignored_words

    # Calculate how much generated vocabulary
    # exists in the source notes
    total_generated_words = len(
        generated_words - ignored_words
    )

    if total_generated_words == 0:
        return False

    grounded_words = (
        generated_words
        - ignored_words
    ) & source_words

    grounding_score = (
        len(grounded_words)
        / total_generated_words
    )

    return grounding_score >= 0.50
