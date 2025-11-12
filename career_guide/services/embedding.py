from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    if not text.strip():
        raise ValueError("Empty text provided for embedding")
    return model.encode(text).tolist()
