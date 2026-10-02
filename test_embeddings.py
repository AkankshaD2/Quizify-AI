from sentence_transformers import SentenceTransformer
import numpy as np


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


sentences = [
    "The MAC layer controls channel access.",
    "IoT devices access the communication channel.",
    "Python is a programming language."
]


# Convert sentences into vectors
embeddings = model.encode(sentences)


# Create a query
query = "How do IoT devices access the communication channel?"


# Convert query into a vector
query_embedding = model.encode([query])[0]


# Calculate cosine similarity
similarities = np.dot(embeddings, query_embedding) / (
    np.linalg.norm(embeddings, axis=1) *
    np.linalg.norm(query_embedding)
)


# Display results
for sentence, score in zip(sentences, similarities):

    print("Sentence:", sentence)
    print("Similarity:", score)
    print("-" * 50)
