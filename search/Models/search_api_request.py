from pydantic import BaseModel, Field
from .question import Question


class SearchAPIRequest(BaseModel):
    question: Question