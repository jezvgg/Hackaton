from pydantic import BaseModel, Field
from .sparce_vector import SparseVector


class SparseEmbeddingResponse(BaseModel):
    vectors: list[SparseVector]