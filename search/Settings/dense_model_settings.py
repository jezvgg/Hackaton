from pydantic import BaseModel, Field
import os


class DenseModelSettings(BaseModel):
    url: str
    model_name: str

    @staticmethod
    def from_env() -> "DenseModelSettings":
        return DenseModelSettings(
            model_name = os.getenv("EMBEDDINGS_DENSE_MODEL", "Qwen/Qwen3-Embedding-0.6B"),
            url = os.getenv('EMBEDDINGS_DENSE_URL')
        )