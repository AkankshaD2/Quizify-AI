
from .structure_detector import detect_unit, detect_topic, detect_section
from .cleaner import is_noise


def build_structure(paragraphs):
    structured_data = []

    current_unit = None
    current_topic = None
    current_section = None

    # Check whether the document uses Word heading styles
    uses_word_headings = any(
        paragraph["style"].startswith("Heading")
        for paragraph in paragraphs
    )

    for paragraph in paragraphs:

        text = paragraph["text"]
        style = paragraph["style"]

        if is_noise(text):
            continue

        # Handle documents using Word heading styles
        if uses_word_headings:

            if style == "Heading 1":
                current_unit = text
                current_topic = text
                current_section = "Content"
                continue

            elif style in ("Heading 2", "Heading 3"):
                current_topic = text
                current_section = "Content"
                continue

            elif style in ("Title", "Subtitle"):
                continue

        # Handle documents using the original heading patterns
        else:

            if detect_unit(text):
                current_unit = text
                current_topic = None
                current_section = None
                continue

            if detect_topic(text):
                current_topic = text
                current_section = None
                continue

            if detect_section(text):
                current_section = text
                continue

        # Store content under the detected headings
        if current_unit and current_topic and current_section:
            structured_data.append({
                "unit": current_unit,
                "topic": current_topic,
                "section": current_section,
                "content": text
            })

    return structured_data
