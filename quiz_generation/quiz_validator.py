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
        return True

    for number in numbers:

        if number not in source_text:

            print(
                "Unsupported numeric value found:"
            )

            print(
                number
            )

            return False

    return True



def validate_correct_answer(question, chunk):
    """
    Validate the correct answer using exact matching
    or conservative word-overlap matching.
    """

    _, _, content = get_chunk_context(chunk)

    source_text = normalize_text(content)
    correct_answer = normalize_text(
        get_answer_text(question)
    )

    correct_answer = re.sub(
        r"^(a|an|the)\s+",
        "",
        correct_answer
    )

    print("\n===== CORRECT ANSWER =====")
    print(correct_answer)
    print("==========================")

    if not correct_answer:
        print("Correct answer validation: FAILED")
        return False

    # First: check for an exact source match.
    if correct_answer in source_text:
        print("Direct source match: PASSED")
        return True

    # Second: check meaningful word overlap.
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were",
        "be", "been", "being", "do", "does", "did",
        "has", "have", "had", "to", "of", "in", "on",
        "for", "with", "and", "or", "but", "this",
        "that", "these", "those", "it","they", "its"
    }

    answer_words = {
        word for word in correct_answer.split()
        if word not in stop_words
    }

    source_words = set(source_text.split())

    if not answer_words:
        print("Correct answer validation: FAILED")
        return False

# Treat common equivalent wording conservatively.
    equivalent_words = {
        "how": "way",
        "way": "how"
    }

    matched_words = {
        word for word in answer_words
        if (
            word in source_words
            or equivalent_words.get(word) in source_words
        )
    }

    overlap = len(matched_words) / len(answer_words)

    print(f"Meaningful word overlap: {overlap:.2%}")

    if overlap >= 0.85:
        print("Word overlap validation: PASSED")
        return True

    print("Correct answer validation: FAILED")
    return False



def validate_explanation(question, chunk):
    """
    Validate that the explanation is non-empty and
    uses information supported by the source.
    """

    topic, section, content = get_chunk_context(chunk)

    explanation = normalize_text(question.explanation)
    source_text = normalize_text(content)

    print("\n===== EXPLANATION VALIDATION =====")

    if not explanation:
        print("Explanation is empty.")
        return False

    # Words that may be used to explain source information.
    SAFE_EXPLANATION_WORDS = {
        "explicitly", "explicit", "listed", "list",
        "as", "feature", "features", "advantage",
        "advantages", "limitation", "limitations",
        "definition", "according", "to", "notes",
        "note", "study", "source", "states", "stated",
        "mentioned", "mention", "directly", "given",
        "provided", "shows", "shown", "indicates",
        "indicated", "is", "are", "was", "were",
        "the", "a", "an", "of", "for", "in", "on",
        "this", "that", "it", "its", "described",
        "supplied", "correct", "answer", "supported",
        "by", "uses", "using", "protocol",
        "communication", "model", "application",
        "layer", "over", "according", "which",
        "what", "how", "does", "do", "can",
        "developing", "small", "interactive",
        "basic", "artificial", "intelligence",
        "techniques", "used"
    }

    source_words = set(source_text.split())
    topic_words = set(normalize_text(topic).split())
    section_words = set(normalize_text(section).split())

    allowed_words = (
        source_words
        | topic_words
        | section_words
        | SAFE_EXPLANATION_WORDS
    )

    explanation_words = set(explanation.split())

    unsupported_words = (
        explanation_words - allowed_words
    )

    if unsupported_words:
        print("Unsupported explanation words found:")
        print(", ".join(sorted(unsupported_words)))
        print("Explanation validation: FAILED")
        return False

    print("Explanation source grounding: PASSED")
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
IMPORTANT SECTION AUTHORITY RULE:

If the supplied section is "Features", every fact listed in the supplied content should be treated as a feature of the topic.

If the supplied section is "Advantages", every fact listed in the supplied content should be treated as an advantage.

If the supplied section is "Limitations", every fact listed in the supplied content should be treated as a limitation.

If the supplied section is "Definition", use the supplied definition as authoritative.

Do NOT reject a question merely because multiple answer options are also valid facts from the supplied section. A multiple-choice question may contain several source-supported options as distractors, while exactly one is designated as the correct answer.
IMPORTANT CORRECT-ANSWER RULE:

The correct answer is SUPPOSED to be a fact supported by the supplied source.

If the question asks:
"Which of the following is listed as a feature of LoRaWAN?"

and the source lists:
"Secure Communication"

then an option containing "Secure Communication" is a VALID correct answer.

Do NOT reject a question because the correct answer is also a fact listed in the source.

Being a source-supported fact is exactly what makes the option a valid answer.

The phrase "correct answer" refers to the answer selected for the question. It does NOT mean that the source should describe the answer as "the answer."

For example:

Source:
Long Range
Very Low Power
Low Data Rate
Wide Area Coverage
Secure Communication
High Scalability

Question:
Which of the following is listed as a feature of LoRaWAN?

Correct answer:
Secure Communication

This is VALID because Secure Communication appears in the supplied Features section.

Never treat the relationship:
"Secure Communication is a feature"
as a contradiction merely because "Secure Communication" is marked as the correct answer.
IMPORTANT SECTION SEMANTICS:

The section metadata is authoritative.

If Section = "Features", then EVERY item listed in the supplied content is a feature of the topic, even if the word "feature" does not appear before each item.

For example:

Topic: LoRaWAN
Section: Features

Content:
Long Range
Very Low Power
Low Data Rate
Wide Area Coverage
Secure Communication
High Scalability

This means all six items are features of LoRaWAN.

Therefore:

"Low Data Rate" = feature
"Wide Area Coverage" = feature
"Secure Communication" = feature
"High Scalability" = feature

Do NOT require the source text to repeat the word "feature" beside every individual item.

The section heading "Features" applies to all items in that section.

The same rule applies to other sections:

If Section = "Advantages", every listed item is an advantage.

If Section = "Limitations", every listed item is a limitation.

If Section = "Definition", the supplied content is the authoritative definition.

A question is NOT invalid merely because the source lists multiple valid facts that can appear as answer options. Those facts may be used as distractors.

For example, if all four options are listed under a Features section and one is marked as the correct answer, the question can still be valid because the question asks which option is the designated answer, not whether the other options are false facts.
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
    options={
        "temperature": 0,
        "num_predict": 200,
    },
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

    valid_match = re.findall(
        r"\bVALID:\s*(YES|NO)\b",
        result_upper
    )

    if not valid_match:
        print("Could not parse LLM validation result.")
        return False

    validation_result = valid_match[-1]

    if valid_match:

        decision = valid_match[-1]

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

        print(
        "LLM validation: SKIPPED "
        "(deterministic validation mode)"
    )

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
