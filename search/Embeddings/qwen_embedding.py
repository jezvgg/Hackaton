import httpx

from .abstract_embedding import AbstractEmbedding
from Settings import DenseModelSettings, OpenAPISettings
from Models import DenseEmbeddingResponse


class QwenEmbedding(AbstractEmbedding):
    settings: DenseModelSettings
    api_settings: OpenAPISettings
    client: httpx.AsyncClient
    

    def __init__(self, 
                dense_settings: DenseModelSettings, 
                openapi_settings: OpenAPISettings,
                client: httpx.AsyncClient):
        self.settings = dense_settings
        self.api_settings = openapi_settings
        self.client = client


    def get_upstream_request_kwargs() -> dict[str, object]:
        headers = {"Content-Type": "application/json"}
        kwargs: dict[str, Any] = {"headers": headers}

        if self.api_settings.login and self.api_settings.password:
            kwargs["auth"] = (
                self.self.api_settings.login, 
                self.api_settings.password
                )
            return kwargs

        if self.api_settings.api_key:
            headers["Authorization"] = f"Bearer {self.api_settings.api_key}"

        return kwargs

        
    async def __call__(self, text: str) :
        '''
        Здесь обязательно нужно реализовать все запросы асинхронно,
        при помощи библеотеки httpx,
        для проверки работоспособности можно использовать API:
        https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
        '''
        response = await self.client.post(
            self.settings.url,
            **self.api_settings.get_upstream_request_kwargs(),
            json={
                "model": self.settings.model_name,
                "input": [text],
            },
        )
        response.raise_for_status()

        payload = DenseEmbeddingResponse.model_validate(response.json())
        if not payload.data:
            raise ValueError("Dense embedding response is empty")

        return payload.data[0].embedding