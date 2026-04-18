from pydantic import BaseModel
from Models import DenseEmbeddingItem

class DenseEmbeddingResponse(BaseModel):
    data: list[DenseEmbeddingItem]