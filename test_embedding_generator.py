from document_processing.docx_reader import extract_docx
from document_processing.structure_builder import build_structure
from document_processing.chunker import create_chunks
from document_processing.embedding_generator import generate_embeddings


file_path = "test_documents/notes.docx"


# Step 1: Extract document
paragraphs = extract_docx(file_path)


# Step 2: Build structure
structured_data = build_structure(paragraphs)


# Step 3: Create chunks
chunks = create_chunks(structured_data, max_words=100)


# Step 4: Generate embeddings
chunks = generate_embeddings(chunks)


# Check the result
print("TOTAL CHUNKS:", len(chunks))

print("\nFIRST CHUNK:")
print("Unit:", chunks[0]["unit"])
print("Topic:", chunks[0]["topic"])
print("Section:", chunks[0]["section"])
print("Content:", chunks[0]["content"])

print("\nEmbedding shape:", chunks[0]["embedding"].shape)
