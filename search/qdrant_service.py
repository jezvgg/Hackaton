from qdrant_client import AsyncQdrantClient, models

from Settings import Settings
from Embeddings import QwenEmbedding, BM25Embedding
from Models import SearchAPIResponse, SparseVector


class QDrantService:
    settings: Settings
    dense_embedding: QwenEmbedding
    sparce_embedding: BM25Embedding


    def __init__(self, settings: Settings):
        self.settings = settings
        self.dense_embedding = QwenEmbedding(settings.dense_model, settings.open_api)
        self.sparce_embedding = BM25Embedding(settings.sparce_model_name)
        self.http = httpx.AsyncClient()
        self.qdrant = AsyncQdrantClient(
            url=self.settings.qdrant.url,
            api_key=self.settings.open_api.api_key,
        )

    async def get_rerank_scores(
        self,
        label: str,
        targets: list[str],
    ) -> list[float]:
        if not targets:
            return []

        response = await self.http.post(
            self.settings.rerank.url,
            **get_upstream_request_kwargs(),
            json={
                "model": self.settings.rerank.model_name,
                "encoding_format": "float",
                "text_1": label,
                "text_2": targets,
            },
        )
        response.raise_for_status()

        payload = response.json()
        data = payload.get("data") or []

        return [float(sample["score"]) for sample in data]


    async def rerank(
        self,
        query: str,
        points: list[object],
    ) -> list[object]:
        rerank_candidates = points
        rerank_targets = [point.payload.get("page_content") for point in rerank_candidates]
        scores = await get_rerank_scores(client, query, rerank_targets)

        reranked_candidates = [
            point
            for _, point in sorted(
                zip(scores, rerank_candidates, strict=True),
                key=lambda item: item[0],
                reverse=True,
            )
        ]

        return reranked_candidates[:10]


    async def search(self, query: str) -> list[object]:
        dense_vector, sparce_vector = await asyncio.gather(
                                                self.dense_embedding(self.http, query),
                                                self.sparce_embedding(query),
                                            )
        best_points = await self.__qdrant_search(dense_vector, sparse_vector)

        return best_points


    async def __qdrant_search(
        self,
        dense_vector: list[float],
        sparse_vector: SparseVector,
        ) -> object | None:
        response = await self.qdrant.query_points(
            collection_name=self.qdrant_settings.collection_name,
            prefetch=[
                models.Prefetch(
                    query=dense_vector,
                    using=self.qdrant_settings.dense_name,
                    limit=self.search_settings.dense_prefetch,
                ),
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_vector.indices,
                        values=sparse_vector.values,
                    ),
                    using=self.qdrant_settings.sparce_name,
                    limit=self.search_settings.sparce_prefetch,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=self.search_settings.retrive,
            with_payload=True,
        )

        if not response.points:
            return None

        return response.points