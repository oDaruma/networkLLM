
from __future__ import annotations
from pathlib import Path
from typing import List
import re
import faiss
import numpy as np

def simple_split(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

class SpecIndex:
    def __init__(self):
        self.docs: list[str] = []
        self.index = None

    def add_document(self, text: str) -> None:
        self.docs.extend(simple_split(text))

    def _embed(self, texts: List[str]) -> np.ndarray:
        from collections import Counter
        vocab = {}
        for t in texts:
            for w in re.findall(r"[a-z0-9]+", t.lower()):
                if w not in vocab: vocab[w] = len(vocab)
        X = np.zeros((len(texts), len(vocab)), dtype="float32")
        for i, t in enumerate(texts):
            cnt = Counter(re.findall(r"[a-z0-9]+", t.lower()))
            for w, c in cnt.items():
                X[i, vocab[w]] = c
        # l2 normalise
        X /= np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-9, None)
        return X

    def build(self):
        X = self._embed(self.docs)
        self.index = faiss.IndexFlatIP(X.shape[1])
        self.index.add(X)

    def search(self, query: str, k: int = 5) -> list[str]:
        Xq = self._embed([query])
        D, I = self.index.search(Xq, k)
        return [self.docs[i] for i in I[0]]
