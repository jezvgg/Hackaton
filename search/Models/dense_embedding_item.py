from pydantic import BaseModel, Field


class DenseEmbeddingItem(BaseModel):
    index: int
    embedding: list[float]