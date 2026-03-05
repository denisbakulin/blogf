from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, le=15, default=10)


def search_param_fabric(allowed_fields: type):
    class SearchParams:
        def __init__(
            self,
            # Делаем параметры необязательными или с дефолтами
            value: Annotated[str, Query(min_length=1, description="Значение")],
            field: Annotated[allowed_fields, Query(description="Критерий")],
            strict: Annotated[bool, Query(description="Строгое совпадение")],
        ):
            self.value = value
            self.strict = strict
            self.field = field

    return SearchParams
