from pydantic import BaseModel, Field
import os


class RerankerSettings(BaseModel):
    model_name: str
    url: str

    @staticmethod
    def from_env() -> "RerankerSettings":
        return RerankerSettings(
            model_name = os.genenv('RERANKER_MODEL', "nvidia/llama-nemotron-rerank-1b-v2"),
            url = os.getenv('RERANKER_URL')
        )