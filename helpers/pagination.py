from pydantic import BaseModel, Field


class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, le=15, default=10)
