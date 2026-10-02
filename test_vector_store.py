from document_processing.docx_reader import extract_docx
from document_processing.structure_builder import build_structure
from document_processing.chunker import create_chunks
from document_processing.embedding_generator import generate_embeddings
from document_processing.vector_store import save_embeddings, load_embeddings


file_path = "test_documents/notes.docx"


# Step 1: Extract document
paragraphs = extract_docx(file_path)

# Step 2: Build structure
structured_data = build_structure(paragraphs)

# Step 3: Create chunks
chunks = create_chunks(structured_data, max_words=100)

# Step 4: Generate embeddings
chunks = generate_embeddings(chunks)

# Step 5: Save embeddings
save_embeddings(chunks)

print("✅ Embeddings saved successfully!")


# Step 6: Load embeddings
loaded_chunks = load_embeddings()

print("✅ Embeddings loaded successfully!")

print("Total chunks:", len(loaded_chunks))
print("First embedding shape:", loaded_chunks[0]["embedding"].shape)
