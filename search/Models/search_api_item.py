from pydantic import BaseModel, Field


class SearchAPIItem(BaseModel):
    message_ids: list[str]