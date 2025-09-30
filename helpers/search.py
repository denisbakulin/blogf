from pydantic import BaseModel, Field
from fastapi import Query
from typing import Literal

class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, le=15, default=10)

    def get(self) -> dict[str, int]:
        return dict(
            offset=self.offset,
            limit=self.limit
        )

def search_param_fabric(allowed_fields: type[str]):
    class SearchParams:
        def __init__(
            self,
            q: str = Query(..., min_length=1, description="Значение запроса"),
            field: allowed_fields = Query(..., description="Критерий запроса"),
            strict: bool = Query(..., description="Строгое совпадение"),
        ):
            self.q = q
            self.strict = strict
            self.field = field

    return SearchParams
