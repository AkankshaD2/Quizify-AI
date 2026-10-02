from sentence_transformers import SentenceTransformer


def generate_embeddings(chunks):
    """
    Generate embeddings for all chunks.

    Each chunk keeps its original metadata
    and receives an embedding vector.
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks
