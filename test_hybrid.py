import re


query = "Which protocol is designed for long-range communication with low power consumption?"


texts = {
    "IEEE 802.15.4": """
    IEEE 802.15.4 is a wireless communication standard for low-power IoT devices.
    Low Power Consumption Low Data Rate Short Range
    """,

    "LoRaWAN": """
    LoRaWAN is a Low Power Wide Area Network protocol used for long-range communication in IoT.
    Long Range Very Low Power Low Data Rate Wide Area Coverage
    """
}


def normalize_text(text):
    text = text.lower()

    text = text.replace("-", " ")

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def phrase_matches(query, text):

    query = normalize_text(query)
    text = normalize_text(text)

    phrases = [
        "long range",
        "low power",
        "wide area",
        "low data rate"
    ]

    matches = []

    for phrase in phrases:

        if phrase in query and phrase in text:
            matches.append(phrase)

    return matches


print("QUERY:")
print(query)

for topic, text in texts.items():

    print("\n" + topic)

    matches = phrase_matches(
        query,
        text
    )

    print("Matching phrases:", matches)
