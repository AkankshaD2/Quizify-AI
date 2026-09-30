import re


def clean_text(text):
    text = text.strip()

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    return text
