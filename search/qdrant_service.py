import asyncio

from qdrant_client import AsyncQdrantClient, models
import httpx

from Settings import Settings
from Embeddings import QwenEmbedding, BM25Embedding
from Models import SearchAPIResponse, SparseVector


class QDrantService:
    settings: Settings
    dense_embedding: QwenEmbedding
    sparse_embedding: BM25Embedding
    http: httpx.AsyncClient
    qdrant: AsyncQdrantClient


    def __init__(self, settings: Settings):
        self.settings = settings

        self.http = httpx.AsyncClient()
        self.qdrant = AsyncQdrantClient(
            url=self.settings.qdrant.url,
            api_key=self.settings.open_api.api_key,
        )

        self.dense_embedding = QwenEmbedding(settings.dense_model, settings.open_api, self.http)
        self.sparse_embedding = BM25Embedding(settings.sparce_model_name)

    async def get_rerank_scores(
        self,
        label: str,
        targets: list[str],
    ) -> list[float]:
        if not targets:
            return []

        response = await self.http.post(
            self.settings.rerank.url,
            **self.settings.open_api.get_upstream_request_kwargs(),
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
        rerank_candidates = points[:self.settings.reranker.limit]
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

        return reranked_candidates


    async def search(self, query: str) -> list[object]:
        dense_vector = await self.dense_embedding(query)
        sparse_vector = self.sparse_embedding(query)
        best_points = await self.__qdrant_search(dense_vector, sparse_vector)

        return best_points


    async def __qdrant_search(
        self,
        dense_vector: list[float],
        sparse_vector: SparseVector,
        ) -> object | None:
        response = await self.qdrant.query_points(
            collection_name=self.settings.qdrant.collection_name,
            prefetch=[
                models.Prefetch(
                    query=dense_vector,
                    using=self.settings.qdrant.dense_name,
                    limit=self.settings.search.dense_prefetch,
                ),
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_vector.indices,
                        values=sparse_vector.values,
                    ),
                    using=self.settings.qdrant.sparce_name,
                    limit=self.settings.search.sparce_prefetch,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=self.settings.search.retrive,
            with_payload=True,
        )

        if not response.points:
            return None

        return response.points