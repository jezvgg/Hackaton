from fastembed import SparseTextEmbedding

from .abstract_embedding import AbstractEmbedding
from Models import SparseVector


class BM25Embedding(AbstractEmbedding):
    model: SparseTextEmbedding

    def __init__(self, sparce_model: str): 
        self.model = SparseTextEmbedding(model_name=sparce_model)
        

    def __call__(self, text: str) -> SparseVector:
        vectors = list(self.model.embed([text]))
        if not vectors:
            raise ValueError("Sparse embedding response is empty")

        item = vectors[0]
        return SparseVector(
            indices=[int(index) for index in item.indices.tolist()],
            values=[float(value) for value in item.values.tolist()],
        )