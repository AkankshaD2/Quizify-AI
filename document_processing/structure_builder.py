from .structure_detector import (
    detect_unit,
    detect_topic,
    detect_section
)


def build_structure(paragraphs):

    current_unit = None
    current_topic = None
    current_section = None

    structured_data = []

    for paragraph in paragraphs:

        text = paragraph["text"]

        # Check if paragraph is a unit
        if detect_unit(text):
            current_unit = text
            current_topic = None
            current_section = None
            continue

        # Check if paragraph is a topic
        if detect_topic(text):
            current_topic = text
            current_section = None
            continue

        # Check if paragraph is a section
        if detect_section(text):
            current_section = text
            continue

        # Everything else is content
        if current_unit and current_topic and current_section:

            structured_data.append({
                "unit": current_unit,
                "topic": current_topic,
                "section": current_section,
                "content": text
            })

    return structured_data
