from document_processing.docx_reader import extract_docx


file_path = "test_documents/notes.docx"

paragraphs = extract_docx(file_path)

for paragraph in paragraphs:
    print("STYLE:", paragraph["style"])
    print("TEXT:", paragraph["text"])
    print("-" * 50)
