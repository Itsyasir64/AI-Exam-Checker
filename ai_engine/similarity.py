"""Optional embeddings / cosine-similarity sanity check."""
import numpy as np


def cosine_similarity(a, b) -> float:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / denom) if denom else 0.0


def embed(client, texts, model="text-embedding-3-small"):
    resp = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]


def answer_similarity(client, student_answer: str, answer_key: str) -> float:
    if not student_answer.strip():
        return 0.0
    s, k = embed(client, [student_answer, answer_key])
    return cosine_similarity(s, k)
