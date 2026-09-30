from document_processing.structure_detector import (
    detect_unit,
    detect_topic,
    detect_section
)


test_texts = [
    "UNIT III SUMMARY – Protocols for IoT",
    "1. Physical Layer",
    "2. MAC (Medium Access Control) Layer",
    "10. MQTT",
    "Definition",
    "Functions",
    "Advantages",
    "Limitations",
    "Low Power Consumption",
    "The MAC Layer controls how multiple IoT devices access the communication channel."
]


for text in test_texts:

    print("TEXT:", text)

    print("UNIT:", detect_unit(text))
    print("TOPIC:", detect_topic(text))
    print("SECTION:", detect_section(text))

    print("-" * 50)
