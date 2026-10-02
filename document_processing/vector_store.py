import pickle


def save_embeddings(chunks, file_path="embeddings.pkl"):
    """
    Save chunks and their embeddings to a file.
    """

    with open(file_path, "wb") as file:
        pickle.dump(chunks, file)


def load_embeddings(file_path="embeddings.pkl"):
    """
    Load chunks and their embeddings from a file.
    """

    with open(file_path, "rb") as file:
        chunks = pickle.load(file)

    return chunks
