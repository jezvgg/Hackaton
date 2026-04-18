from pydantic import BaseModel, Field


class QdrantSettings(BaseModel):
    dense_name: str
    sparce_name: str
    url: str
    collection_name: str

    @staticmethod
    def from_env() -> "QdrantSettings":
        return QdrantSettings(
            dense_name = os.getenv("QDRANT_DENSE_VECTOR_NAME", "dense"),
            sparce_name = os.getenv("QDRANT_SPARSE_VECTOR_NAME", "sparse"),
            url = os.getenv("QDRANT_URL"),
            collection_name = os.getenv("QDRANT_COLLECTION_NAME", "evaluation")
        )