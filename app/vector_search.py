from collections import OrderedDict
from typing import Dict, List

import numpy as np
import faiss

from app.models import Product


N_DIM = 512
TOP_K = 3


class ProductSearch:

    @staticmethod
    def cosine_distance(vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 1
        return 1 - np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    @staticmethod
    def text_matching(query_str: str, paragraph: str) -> bool:
        words = query_str.split(" ")
        return any(w for w in words if w in paragraph)

    @classmethod
    def search_from_cached(
        cls, products: Dict[int, Product],
        embedding: List[float],
    ):
        filtered = {}
        embeddings = []
        tmp = []
        # TODO

        for idx, p in products.items():
            tmp.append((idx, p))
            embeddings.append(p.product_description_vector)
        index = faiss.IndexFlatL2(N_DIM)
        embeddings_array = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_array)
        query_vector = np.array(embedding, dtype=np.float32).reshape(1, -1)
        d, i = index.search(x=query_vector, k=3)
        idx_arr = np.array(i).flatten()
        for i in idx_arr:
            filtered[tmp[i][0]] = tmp[i][1]
        return filtered
