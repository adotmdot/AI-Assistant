import hashlib
import numpy as np

EMBED_DIM = 128

def embed_texts(texts: list[str]):
    vectors = []
    for text in texts:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = np.frombuffer(h, dtype=np.uint8).astype("float32")
        vectors.append(vec[:EMBED_DIM])
    return vectors
