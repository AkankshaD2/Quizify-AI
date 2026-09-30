import re


SECTION_NAMES = {
    "definition",
    "functions",
    "features",
    "advantages",
    "limitations"
}


def detect_unit(text):
    """
    Detect whether the paragraph represents a unit.
    """

    pattern = r"^UNIT\s+[IVXLC0-9]+"

    if re.search(pattern, text, re.IGNORECASE):
        return True

    return False


def detect_topic(text):
    """
    Detect numbered topics such as:
    1. Physical Layer
    2. MAC Layer
    10. MQTT
    """

    pattern = r"^\d+\.\s+.+"

    return bool(re.match(pattern, text))


def detect_section(text):
    """
    Detect common section names.
    """

    return text.lower() in SECTION_NAMES
