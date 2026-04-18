from .dense_model_settings import DenseModelSettings
from .open_api_settings import OpenAPISettings
from .qdrant_settings import QdrantSettings
from .reranker_model import RerankerSettings
from .web_server_settings import WebServerSettings
from .serach_settings import SearchSettings

from pydantic import BaseModel, Field, model_validator


class Settings(BaseModel):
    dense_model: DenseModelSettings
    open_api: OpenAPISettings
    qdrant: QdrantSettings
    reranker: RerankerSettings
    web_server: WebServerSettings
    sparce_model_name: str

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            dense_model = DenseModelSettings.from_env(),
            open_api = OpenAPISettings.from_env(),
            qdrant = QdrantSettings.from_env(),
            reranker = RerankerSettings.from_env(),
            web_server = WebServerSettings.from_env(),
            sparce_model_name = os.getenv('SPARSE_MODEL_NAME', "Qdrant/bm25"),
            serach_settings = SearchSettings.from_env()
        )

    @model_validator(mode='after')
    def check_passwords_match(self):
        if bool(self.open_api.login) != bool(self.open_api.password):
            raise RuntimeError("OPEN_API_LOGIN and OPEN_API_PASSWORD must be set together")

        if not self.open_api.api_key and not (self.open_api.login and self.open_api.password):
            raise RuntimeError("Either API_KEY or OPEN_API_LOGIN and OPEN_API_PASSWORD must be set")

        return self
