from docx import Document
from .cleaner import clean_text


def extract_docx(file_path):
    doc = Document(file_path)

    paragraphs = []

    for paragraph in doc.paragraphs:

        text = clean_text(paragraph.text)

        if text:
            paragraphs.append({
                "text": text,
                "style": paragraph.style.name
            })

    return paragraphs
