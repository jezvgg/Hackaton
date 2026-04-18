from pydantic import BaseModel, Field
import os


class SearchSettings(BaseModel):
    dense_prefetch: int
    sparce_prefetch: int
    retrive: int
    rerank_limit: int

    @staticmethod
    def from_env() -> "SearchSettings":
        return SearchSettings(
            dense_prefetch = os.getenv('DENSE_PREFETCH_K', 10),
            sparce_prefetch = os.getenv('SPARCE_PREFETCH_K', 30),
            retrive = os.getenv('RETRIVE_K', 20),
            rerank_limit = os.getenv('RERANK_LIMIT', 10)
        )