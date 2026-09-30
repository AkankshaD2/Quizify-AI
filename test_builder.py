from document_processing.docx_reader import extract_docx
from document_processing.structure_builder import build_structure


file_path = "test_documents/notes.docx"

# Step 1: Extract the document
paragraphs = extract_docx(file_path)

# Step 2: Build structured data
structured_data = build_structure(paragraphs)

# Step 3: Display the result
for item in structured_data[:20]:

    print("UNIT:", item["unit"])
    print("TOPIC:", item["topic"])
    print("SECTION:", item["section"])
    print("CONTENT:", item["content"])
    print("-" * 60)
