import re


def clean_text(text):
    text = text.strip()

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # Fix known spacing issues from document extraction
    fixes = {
        "accessthe": "access the",
        "forLow-Rate": "for Low-Rate",
        "usingUDP": "using UDP",
        "usingthe": "using the",
        "overthe": "over the",
        "utilizationReliable": "utilization Reliable",
    }

    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)

    return text


def is_noise(text):
    noise_phrases = [
        "5-Minute Final Revision",
        "Top of Form",
        "Bottom of Form"
    ]

    for phrase in noise_phrases:
        if phrase.lower() in text.lower():
            return True

    return False
