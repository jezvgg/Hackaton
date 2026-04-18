from pydantic import BaseModel, Field
from .search_api_item import SearchAPIItem


class SearchAPIResponse(BaseModel):
    results: list[SearchAPIItem]