from document_processing.docx_reader import extract_docx
from document_processing.structure_builder import build_structure
from document_processing.chunker import create_chunks


file_path = "test_documents/notes.docx"

# Extract document
paragraphs = extract_docx(file_path)

# Build structure
structured_data = build_structure(paragraphs)

# Create chunks
chunks = create_chunks(structured_data, max_words=100)

# Display chunks
for index, chunk in enumerate(chunks[:10], start=1):

    print("CHUNK:", index)
    print("UNIT:", chunk["unit"])
    print("TOPIC:", chunk["topic"])
    print("SECTION:", chunk["section"])
    print("CONTENT:", chunk["content"])
    print("-" * 70)
print("TOTAL CHUNKS:", len(chunks))

for chunk in chunks:
    assert chunk["unit"]
    assert chunk["topic"]
    assert chunk["section"]
    assert chunk["content"]

print("✅ All chunks passed validation!")
