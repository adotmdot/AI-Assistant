import os
import faiss
import numpy as np

class FaissStore:
    def __init__(self, embed_fn):
        self.embed_fn = embed_fn
        self.texts = []
        self.metas = []
        self.index = None

    def build(self, docs_path="app/docs"):
        for fn in os.listdir(docs_path):
            path = f"{docs_path}/{fn}"
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                self.texts.append(text)
                self.metas.append({"source": fn})

        embeddings = self.embed_fn(self.texts)
        vectors = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)

    def search(self, query, k=3):
        q = np.array(self.embed_fn([query])).astype("float32")
        scores, ids = self.index.search(q, k)

        results = []
        for i in ids[0]:
            results.append({
                "text": self.texts[i],
                "source": self.metas[i]["source"]
            })
        return results
