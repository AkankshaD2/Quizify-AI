import re

from ollama import chat


def normalize_text(text):
    """
    Normalize text for reliable comparison.
    """

    text = str(text).lower()

    text = text.replace("-", " ")

    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_chunk_context(chunk):
    """
    Return topic, section, and content from a chunk.

    Supports dictionary chunks and simple string chunks.
    """

    if isinstance(chunk, dict):

        topic = chunk.get(
            "topic",
            ""
        )

        section = chunk.get(
            "section",
            ""
        )

        content = chunk.get(
            "content",
            ""
        )

        return topic, section, content

    return "", "", str(chunk)


def get_answer_text(question):
    """
    Return the actual answer text from the selected
    answer option.
    """

    answer = str(
        question.correct_answer
    ).strip()

    options = question.options

    if hasattr(options, answer):

        return str(
            getattr(options, answer)
        ).strip()

    return answer


def extract_source_facts(chunk):
    """
    Extract meaningful source facts.

    The source content is already structured into
    topic/section chunks, so normalized content is
    sufficient for deterministic grounding.
    """

    topic, section, content = get_chunk_context(
        chunk
    )

    source_text = normalize_text(
        content
    )

    return {
        "topic": normalize_text(topic),
        "section": normalize_text(section),
        "content": source_text,
    }


def validate_numeric_grounding(question, chunk):
    """
    Validate numeric values appearing in the question
    or correct answer.

    Any numeric quantity used by the generated quiz
    must appear in the supplied source.
    """

    _, _, content = get_chunk_context(
        chunk
    )

    source_text = normalize_text(
        content
    )

    question_text = normalize_text(
        question.question
    )

    answer_text = normalize_text(
        get_answer_text(question)
    )

    combined_text = (
        question_text
        + " "
        + answer_text
    )

    numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        combined_text
    )

    if not numbers:

        print(
            "Numeric/quantity grounding: PASSED"
        )

        return True

    for number in numbers:

        if number not in source_text:

            print(
                "Unsupported numeric value found:"
            )

            print(
                number
            )

            print(
                "Numeric/quantity grounding: FAILED"
            )

            return False

    print(
        "Numeric/quantity grounding: PASSED"
    )

    return True


def validate_correct_answer(question, chunk):
    """
    Deterministically validate the correct answer.

    The complete answer phrase must appear in the
    source content.
    """

    _, _, content = get_chunk_context(
        chunk
    )

    source_text = normalize_text(
        content
    )

    correct_answer = normalize_text(
        get_answer_text(question)
    )

    # Remove harmless article prefixes.
    correct_answer = re.sub(
        r"^(a|an|the)\s+",
        "",
        correct_answer
    )

    print(
        "\n===== CORRECT ANSWER ====="
    )

    print(
        correct_answer
    )

    print(
        "=========================="
    )

    if not correct_answer:

        print(
            "Correct answer validation: FAILED"
        )

        return False

    if correct_answer in source_text:

        print(
            "Direct source match: PASSED"
        )

        return True

    print(
        "Exact answer phrase not found in source: FAILED"
    )

    return False


def validate_explanation(question, chunk):
    """
    Deterministically validate the explanation.

    The explanation must:
    - contain the correct answer
    - use words supported by the source
      or harmless explanation scaffolding
    """

    topic, section, content = get_chunk_context(
        chunk
    )

    explanation = normalize_text(
        question.explanation
    )

    correct_answer = normalize_text(
        get_answer_text(question)
    )

    # Remove harmless article prefixes.
    correct_answer = re.sub(
        r"^(a|an|the)\s+",
        "",
        correct_answer
    )

    source_text = normalize_text(
        content
    )

    print(
        "\n===== EXPLANATION VALIDATION ====="
    )

    if not explanation:

        print(
            "Explanation is empty."
        )

        return False

    print(
        "\n===== EXPLANATION DEBUG ====="
    )

    print(
        "Correct answer:"
    )

    print(
        correct_answer
    )

    print(
        "Explanation:"
    )

    print(
        explanation
    )

    print(
        "============================"
    )

    if correct_answer not in explanation:

        print(
            "Correct answer does not appear "
            "in explanation."
        )

        return False

    SAFE_EXPLANATION_WORDS = {
        "explicitly",
        "explicit",
        "listed",
        "list",
        "as",
        "feature",
        "features",
        "advantage",
        "advantages",
        "limitation",
        "limitations",
        "definition",
        "according",
        "to",
        "notes",
        "note",
        "study",
        "source",
        "states",
        "stated",
        "mentioned",
        "mention",
        "directly",
        "given",
        "provided",
        "shows",
        "shown",
        "indicates",
        "indicated",
        "is",
        "are",
        "was",
        "were",
        "the",
        "a",
        "an",
        "of",
        "for",
        "in",
        "on",
        "this",
        "that",
        "it",
        "its",
        "described",
        "supplied",
        "correct",
        "answer",
        "supported",
        "by",
        "uses",
        "using",
        "protocol",
        "communication",
        "model",
        "application",
        "layer",
        "over",
        "according",
    }

    source_words = set(
        source_text.split()
    )

    topic_words = set(
        normalize_text(topic).split()
    )

    section_words = set(
        normalize_text(section).split()
    )

    allowed_words = (
        source_words
        | topic_words
        | section_words
        | SAFE_EXPLANATION_WORDS
    )

    explanation_words = explanation.split()

    unsupported_words = []

    for word in explanation_words:

        if word in allowed_words:
            continue

        unsupported_words.append(
            word
        )

    if unsupported_words:

        print(
            "Unsupported explanation words found:"
        )

        print(
            ", ".join(
                unsupported_words
            )
        )

        print(
            "Explanation validation: FAILED"
        )

        return False

    section_lower = normalize_text(
        section
    )

    if section_lower == "features":

        print(
            "Feature explanation: PASSED"
        )

        return True

    if section_lower == "advantages":

        print(
            "Advantage explanation: PASSED"
        )

        return True

    if section_lower == "limitations":

        print(
            "Limitation explanation: PASSED"
        )

        return True

    if section_lower == "definition":

        print(
            "Definition explanation: PASSED"
        )

        return True

    print(
        "Explanation source grounding: PASSED"
    )

    return True


def llm_validate_question(question, chunk):
    """
    Secondary LLM sanity check.

    Deterministic validation is the primary authority.

    The LLM validator only checks whether the generated
    question clearly contradicts or misrepresents the
    supplied source.

    It must NOT:
    - require distractors to appear in the source
    - assume the correct answer must be globally unique
    - use outside knowledge
    - reject a question because another real-world
      possibility may exist
    """

    topic, section, content = get_chunk_context(
        chunk
    )

    prompt = f"""
You are a secondary validator for a quiz-generation system.

The deterministic validation system has already verified that:

1. The correct answer appears in the supplied source.
2. The explanation is grounded in the supplied source.
3. The answer and explanation do not contain unsupported
   source facts.

Your ONLY job is to check whether the generated question
clearly contradicts or misrepresents the supplied source.

============================================================
SOURCE
============================================================

Topic:
{topic}

Section:
{section}

Study notes:
{content}

============================================================
GENERATED QUESTION
============================================================

Question:
{question.question}

A: {question.options.A}

B: {question.options.B}

C: {question.options.C}

D: {question.options.D}

Correct answer:
{question.correct_answer}: {get_answer_text(question)}

Explanation:
{question.explanation}

============================================================
VALIDATION RULES
============================================================

1. Use ONLY the supplied study notes.

2. Do NOT use outside knowledge.

3. The correct answer must be supported by the
   supplied study notes.

4. The explanation must be consistent with the
   supplied study notes.

5. Do NOT require the study notes to define every
   technical term used in the question.

6. Do NOT reject a question merely because the source
   does not explain the meaning of a term.

7. If a term or answer appears directly in the study
   notes and the question asks about that fact,
   consider it supported.

8. Do NOT reject a question because a distractor
   option is not present in the study notes.

9. Do NOT reject a question because a distractor
   option IS present in the study notes.

10. Your job is NOT to determine whether every option
    is supported by the source.

11. Only the intended correct answer must be supported
    by the source.

12. The explanation only needs to justify the correct
    answer.

13. The explanation does NOT need to explain why every
    distractor is incorrect.

14. Do NOT reject a question because another protocol,
    technology, or concept could theoretically have
    similar properties in the real world.

15. Do NOT use outside knowledge to determine whether
    the correct answer is unique in the real world.

16. Do NOT infer uniqueness, exclusivity, or "only"
    claims unless the question explicitly contains
    words such as:

    only
    the only
    exclusively
    always
    never
    all
    every

17. If the supplied source directly supports the
    relationship between the topic and the correct
    answer, consider the question valid unless the
    question explicitly makes a stronger claim than
    the source.

18. Do NOT reject a question because the source does
    not prove that the correct answer is the only
    possible answer in the real world.

19. Do NOT reject a question because another real-world
    possibility may exist.

20. Do NOT add unstated real-world assumptions to
    the question.

21. Do NOT require the source to prove facts that are
    not being tested.

22. Do NOT reject a question merely because the wording
    could have a broader interpretation outside the
    supplied study notes.

============================================================
SECTION AUTHORITY
============================================================

The supplied Section is authoritative.

If Section is:

Features

Then facts from the source must be treated as
features.

If Section is:

Advantages

Then facts from the source must be treated as
advantages.

If Section is:

Limitations

Then facts from the source must be treated as
limitations.

If Section is:

Definition

Then the question must remain directly consistent
with the supplied definition.

Do NOT change the relationship represented by the
Section.

============================================================
MULTIPLE-CHOICE RULE
============================================================

This is a multiple-choice question.

The deterministic validator has already checked
the selected correct answer.

The LLM validator must NOT reject the question because:

- a distractor is not in the source
- a distractor is in the source
- multiple options happen to appear in the source
- another real-world answer could theoretically exist
- the source does not prove global uniqueness

For example:

SOURCE:

Long Range
Very Low Power
Low Data Rate
Wide Area Coverage
Secure Communication
High Scalability

QUESTION:

Which of the following is listed as a feature of LoRaWAN?

A: Low Data Rate
B: Wide Area Coverage
C: Secure Communication
D: High Scalability

Correct answer:
D: High Scalability

This question is VALID because the correct answer
is explicitly supported by the supplied source.

Do NOT reject it merely because A, B, and C also
appear in the source.

============================================================
EXAMPLE: MQTT
============================================================

SOURCE:

MQTT is a lightweight application layer protocol
using the Publish-Subscribe communication model
over TCP.

QUESTION:

What is the application layer protocol using the
Publish-Subscribe communication model over TCP?

A: TCP/IP
B: HTTP
C: MQTT
D: FTP

Correct answer:
C: MQTT

This question is VALID.

The source directly supports the relationship:

MQTT
-> application layer protocol
-> Publish-Subscribe model
-> over TCP

Do NOT reject this question by assuming that it
claims MQTT is the only protocol in the world that
could have these properties.

Do NOT introduce outside protocol knowledge.

============================================================
WHEN TO RETURN VALID: NO
============================================================

Return VALID: NO ONLY when there is a clear problem
supported by the supplied source, such as:

- the question contradicts the source
- the correct answer contradicts the source
- the explanation contradicts the source
- the question assigns a source fact to the wrong topic
- the question assigns a source fact to the wrong section
- the question introduces a factual claim in the
  question itself that is unsupported by the source
- the question changes the meaning of the source
- the question explicitly makes a stronger claim than
  the source supports

Do NOT return VALID: NO because:

- a distractor is unsupported
- a distractor is supported
- multiple distractors appear in the source
- another protocol could theoretically have the
  same property
- the source does not prove global uniqueness
- outside knowledge suggests another possibility
- the question could have a broader interpretation
  outside the study notes

============================================================
DECISION
============================================================

Return exactly ONE of these:

VALID: YES

or

VALID: NO

Choose VALID: YES when:

- the question is supported by the source,
- the correct answer is supported by the source,
- the explanation is consistent with the source,
- and there is no clear contradiction or
  misrepresentation.

Choose VALID: NO ONLY when there is a clear
source-grounded contradiction, wrong relationship,
or unsupported factual claim in the question,
correct answer, or explanation.

If your reasoning says that the question is supported,
accurate, consistent, or does not contradict the source,
you MUST return:

VALID: YES

Do not return VALID: NO when your own reasoning says
the question is valid.

Your final decision must be based ONLY on the supplied
study notes.

============================================================
FINAL OUTPUT
============================================================

Return the decision:

VALID: YES

or:

VALID: NO

You may provide a short reason before or after the
decision, but the final classification MUST contain
exactly one of the two valid labels.
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    result = response.message.content.strip()

    print(
        "\n===== LLM VALIDATION ====="
    )

    print(
        result
    )

    print(
        "=========================="
    )

    result_upper = result.upper()

    valid_match = re.search(
        r"\bVALID:\s*(YES|NO)\b",
        result_upper
    )

    if valid_match:

        decision = valid_match.group(1)

        if decision == "YES":

            return True

        if decision == "NO":

            print(
                "LLM validator rejected the question."
            )

            return False

    print(
        "LLM validator returned an unclear result."
    )

    return False


def validate_question(question, chunk):
    """
    Run all validation checks on a generated quiz question.
    """

    print(
        "\n================================"
    )

    print(
        "      QUIZ VALIDATION START"
    )

    print(
        "================================"
    )

    numeric_valid = validate_numeric_grounding(
        question,
        chunk
    )

    print(
        f"Numeric/quantity grounding: "
        f"{'PASSED' if numeric_valid else 'FAILED'}"
    )

    if not numeric_valid:

        print(
            "Final validation result: False"
        )

        return False

    correct_answer_valid = validate_correct_answer(
        question,
        chunk
    )

    print(
        "Correct answer validation: "
        f"{'PASSED' if correct_answer_valid else 'FAILED'}"
    )

    if not correct_answer_valid:

        print(
            "Final validation result: False"
        )

        return False

    explanation_valid = validate_explanation(
        question,
        chunk
    )

    print(
        "Explanation validation: "
        f"{'PASSED' if explanation_valid else 'FAILED'}"
    )

    if not explanation_valid:

        print(
            "Final validation result: False"
        )

        return False

    llm_valid = llm_validate_question(
        question,
        chunk
    )

    print(
        "LLM validation: "
        f"{'PASSED' if llm_valid else 'FAILED'}"
    )

    if not llm_valid:

        print(
            "Final validation result: False"
        )

        return False

    print(
        "\n================================"
    )

    print(
        "   QUIZ VALIDATION SUCCESS"
    )

    print(
        "================================"
    )

    print(
        "Final validation result: True"
    )

    return True
