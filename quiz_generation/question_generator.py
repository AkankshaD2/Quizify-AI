import re
import json
from ollama import chat
from pydantic import ValidationError

from quiz_generation.quiz_schema import (
    QuizQuestion,
    QuizOptions,
)

from quiz_generation.quiz_validator import (
    validate_question,
)


def clean_text(text):
    """
    Normalize text for comparisons.
    """

    text = str(text)

    text = text.replace(
        "\n",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_llm_response(response_text):
    """
    Parse the structured JSON response returned by Ollama.
    """

    response_text = response_text.strip()

    try:
        data = json.loads(response_text)

    except json.JSONDecodeError:
        print("Failed to parse LLM JSON response.")
        return {}

    parsed = {
        "question": data.get("question", ""),
        "A": data.get("options", {}).get("A", ""),
        "B": data.get("options", {}).get("B", ""),
        "C": data.get("options", {}).get("C", ""),
        "D": data.get("options", {}).get("D", ""),
        "answer": data.get("correct_answer", ""),
        "explanation": data.get("explanation", ""),
        "difficulty": data.get("difficulty", ""),
    }

    return parsed


def validate_basic_structure(parsed):
    """
    Check whether the LLM returned all required fields.
    """

    required_fields = [
        "question",
        "A",
        "B",
        "C",
        "D",
        "answer",
        "explanation",
        "difficulty",
    ]

    for field in required_fields:

        if not parsed.get(field):

            print(
                f"Missing field from LLM response: {field}"
            )

            return False

    return True


def validate_answer_letter(answer):
    """
    Ensure the answer is exactly A, B, C, or D.
    """

    answer = answer.strip().upper()

    return answer in {
        "A",
        "B",
        "C",
        "D",
    }


def validate_unique_options(parsed):
    """
    Ensure all four options are unique.
    """

    options = [
        parsed["A"],
        parsed["B"],
        parsed["C"],
        parsed["D"],
    ]

    normalized_options = [
        clean_text(option).lower()
        for option in options
    ]

    if len(set(normalized_options)) != 4:

        print(
            "Duplicate options detected."
        )

        return False

    return True


def validate_correct_answer_occurs_once(parsed):
    """
    Ensure the correct answer appears exactly once
    among the four options.
    """

    answer_letter = (
        parsed["answer"]
        .strip()
        .upper()
    )

    if not validate_answer_letter(
        answer_letter
    ):

        print(
            "Invalid answer letter."
        )

        return False

    correct_option = clean_text(
        parsed[answer_letter]
    ).lower()

    option_values = [
        clean_text(parsed["A"]).lower(),
        clean_text(parsed["B"]).lower(),
        clean_text(parsed["C"]).lower(),
        clean_text(parsed["D"]).lower(),
    ]

    occurrences = option_values.count(
        correct_option
    )

    if occurrences != 1:

        print(
            "Correct answer does not occur exactly once."
        )

        return False

    return True


def build_prompt(chunk):
    """
    Build a strict grounding prompt for the LLM.
    """

    topic = chunk["topic"]
    section = chunk["section"]
    content = chunk["content"]

    prompt = f"""
You are generating ONE multiple-choice quiz question
from supplied study notes.

Your question MUST be completely grounded in the
supplied study notes.

============================================================
SOURCE CONTEXT
============================================================

Topic:
{topic}

Section:
{section}

Study notes:
{content}

============================================================
GROUNDING RULES
============================================================

1. Use ONLY the supplied study notes.

2. Do NOT use outside knowledge.

3. The question, correct answer, and explanation
   must be grounded in the supplied study notes.

   Distractor options are exempt from this rule,
   provided they are not presented as supported facts
   about the study topic.

4. The correct answer MUST appear literally in the
   supplied study notes.

5. Prefer exact terminology from the study notes.

6. Do NOT paraphrase a source fact into a stronger
   or different claim.

7. Do NOT invent relationships between the topic
   and a fact.

8. Do NOT add unsupported claims about what the
   protocol "helps", "allows", "provides",
   "supports", "ensures", or "enables".

9. Do NOT use unsupported adjectives such as:

important
key
major
primary
common
commonly
typical
typically
essential

10. Do NOT use unsupported relationship phrases such as:

described as
described as a
described as the
referred to as
known as
known for
characterized as
considered
regarded as

11. When the source directly lists a fact under
a section, ask about that fact directly.

For example:

Topic:
5. LoRaWAN

Section:
Features

Study notes:
Long Range
Very Low Power
Low Data Rate
Wide Area Coverage
Secure Communication
High Scalability

GOOD:
Which of the following is listed as a feature of LoRaWAN?

BAD:
Which feature of LoRaWAN is described as Secure Communication?

BAD:
What is LoRaWAN known for regarding Secure Communication?

12. The supplied Section is AUTHORITATIVE.

13. If Section is "Features":
    The question MUST refer to source facts as
    features. Never call them advantages or limitations.

14. If Section is "Advantages":
    The question MUST refer to source facts as
    advantages. Never call them features or limitations.

15. If Section is "Limitations":
    The question MUST refer to source facts as
    limitations. Never call them features or advantages.

16. If Section is "Definition":
    Stay directly consistent with the supplied definition.

17. NEVER change the relationship represented by the
    Section.

For example:

Section:
Features

GOOD:
Which of the following is listed as a feature of LoRaWAN?

BAD:
Which of the following is listed as an advantage of LoRaWAN?

BAD:
Which feature of LoRaWAN is described as an advantage?

Section:
Advantages

GOOD:
Which of the following is listed as an advantage of LoRaWAN?

BAD:
Which of the following is listed as a feature of LoRaWAN?

============================================================
OPTION RULES
============================================================



16. Generate exactly four options:

A
B
C
D

17. All four options MUST be unique.

18. Never repeat an option, word-for-word or
    with only superficial formatting differences.

19. Do NOT use the same answer more than once,
    even if it appears in different capitalization,
    punctuation, or wording.

20. Before submitting the question, compare A, B,
    C, and D with each other and silently verify
    that no two options mean the same thing.

21. Do NOT create distractors by simply extracting
    different words from the same sentence when
    doing so creates duplicate or meaningless options.

22. Every option must be a distinct possible answer
    to the question.

23. The generated question must directly test the
    information requested by the source query.

24. Do not replace the requested concept with another
    fact merely because that fact appears in the source.

25. If the requested concept is "Publish-Subscribe",
    the question and correct answer must test
    "Publish-Subscribe", not TCP, UDP, or another
    unrelated source term.
26. Never use multiple source facts from the same
    section as options when the question asks:

    "Which of the following is listed as a
    feature/advantage/limitation?"

    unless the question is explicitly designed to
    have only one correct source fact.

27. For example, if the source says:

    Long Range
    Very Low Power
    Low Data Rate
    Wide Area Coverage
    Secure Communication
    High Scalability

    and the question is:

    "Which of the following is listed as a
    feature of LoRaWAN?"

    DO NOT generate:

    A: Low Data Rate
    B: High Scalability
    C: Secure Communication
    D: Wide Area Coverage

    because all four are correct.

28. Instead, generate a question where exactly
    one option matches the requested fact.

29. Example:

    Question:
    Which of the following is listed as a feature
    of LoRaWAN?

    A: Low Data Rate
    B: 64-bit Addressing
    C: Circuit Switching
    D: Token Ring

    Correct answer:
    A

30. The three distractors must not be described
    in the explanation as facts from the study notes.

31. Do NOT create distractors by changing a source
    fact into a false statement about the topic.

32. Do NOT create an option that is another valid
    source fact if doing so would create multiple
    correct answers.

33. Before submitting the question, silently verify:

    - Exactly one option answers the question.
    - The correct option is supported by the source.
    - The other three options do not also answer
      the question.
    - The correct answer letter matches the actual
      correct option.
    - The explanation refers to the actual correct
      option.

============================================================
============================================================
EXPLANATION RULES
============================================================

25. The explanation must use only information
from the supplied study notes.

26. Keep the explanation short.

27. The explanation must directly justify why the
correct answer is supported by the source.

28. For Features:

"<correct answer> is explicitly listed as a feature
of <topic>."

29. For Advantages:

"<correct answer> is explicitly listed as an advantage
of <topic>."

30. For Limitations:

"<correct answer> is explicitly listed as a limitation
of <topic>."

31. For Definition:

Use wording that remains directly consistent with
the supplied definition.

32. Do NOT add extra benefits, purposes, applications,
capabilities, or real-world claims.
EXPLANATION RULE:
Do NOT include the option letter (A, B, C, or D) in the explanation.
Mention the correct answer text directly.
For example:
Correct: "Wide Area Coverage is explicitly listed as a feature of LoRaWAN."
Incorrect: "D: Wide Area Coverage is explicitly listed as a feature of LoRaWAN."
============================================================
DIFFICULTY
============================================================

Choose one:

easy
medium
hard

Difficulty must describe the reasoning required by
the question, not introduce additional facts.
IMPORTANT OUTPUT REQUIREMENT:

You MUST provide all four options:

A:
B:
C:
D:

Never stop after A, B, or C.

You MUST also provide all of these fields:

QUESTION:
A:
B:
C:
D:
ANSWER:
EXPLANATION:
DIFFICULTY:

If any field is missing, the response is invalid.

Before submitting your response, silently check that
QUESTION, A, B, C, D, ANSWER, EXPLANATION, and DIFFICULTY
are all present.
============================================================
MANDATORY OUTPUT FORMAT
============================================================

Your response MUST contain EXACTLY these 8 lines/fields
in this order:

QUESTION: <question>

A: <option A>
B: <option B>
C: <option C>
D: <option D>

ANSWER: <A/B/C/D>

EXPLANATION: <short explanation>

DIFFICULTY: <easy/medium/hard>

IMPORTANT:

- NEVER stop after option D.
- ANSWER is mandatory.
- EXPLANATION is mandatory.
- DIFFICULTY is mandatory.
- Do not end your response after A, B, C, or D.
- After writing D, immediately continue with ANSWER.
- Do not add any text before QUESTION.
- Do not add any text after DIFFICULTY.

Before finishing, silently verify that all 8 fields are present.
"""

    return prompt


def generate_question(chunk):
    """
    Generate one grounded quiz question from a chunk.
    """

    topic = chunk["topic"]
    section = chunk["section"]
    content = chunk["content"]

    prompt = build_prompt(
        chunk
    )

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format=QuizQuestion.model_json_schema(),
        options={
            "temperature": 0.2,
            "num_predict": 500,
        },
    )

    raw_response = (
        response.message.content.strip()
    )

    print(
        "\n===== RAW LLM RESPONSE ====="
    )

    print(
        raw_response
    )

    print(
        "============================"
    )

    # --------------------------------------------------------
    # PARSE
    # --------------------------------------------------------

    parsed = parse_llm_response(
        raw_response
    )

    # --------------------------------------------------------
    # BASIC STRUCTURE
    # --------------------------------------------------------

    if not validate_basic_structure(
        parsed
    ):

        raise ValueError(
            "LLM returned an incomplete quiz question."
        )

    # --------------------------------------------------------
    # ANSWER LETTER
    # --------------------------------------------------------

    if not validate_answer_letter(
        parsed["answer"]
    ):

        raise ValueError(
            "LLM returned an invalid answer letter."
        )

    # --------------------------------------------------------
    # UNIQUE OPTIONS
    # --------------------------------------------------------

    if not validate_unique_options(
        parsed
    ):

        raise ValueError(
            "Generated question contains duplicate options."
        )

    # --------------------------------------------------------
    # CORRECT ANSWER OCCURS ONCE
    # --------------------------------------------------------

    if not validate_correct_answer_occurs_once(
        parsed
    ):

        raise ValueError(
            "Correct answer does not occur exactly once."
        )

    # --------------------------------------------------------
    # BUILD PYDANTIC QUESTION
    # --------------------------------------------------------

    try:

        quiz_question = QuizQuestion(
            question=parsed["question"],

            options=QuizOptions(
                A=parsed["A"],
                B=parsed["B"],
                C=parsed["C"],
                D=parsed["D"],
            ),

            correct_answer=parsed[
                "answer"
            ].strip().upper(),

            explanation=parsed[
                "explanation"
            ],

            difficulty=parsed[
                "difficulty"
            ].lower(),
        )

    except ValidationError as error:

        print(
            "\nPydantic validation failed:"
        )

        print(
            error
        )

        raise ValueError(
            "Generated question failed schema validation."
        )

    # --------------------------------------------------------
    # GROUNDING VALIDATION
    # --------------------------------------------------------

    is_valid = validate_question(
        quiz_question,
        chunk
    )

    if not is_valid:

        raise ValueError(
            "Generated question failed grounding validation."
        )

    return quiz_question
