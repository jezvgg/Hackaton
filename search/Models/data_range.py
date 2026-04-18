from pydantic import BaseModel, Field\


class DateRange(BaseModel):
    from_: str = Field(alias="from")
    to: str