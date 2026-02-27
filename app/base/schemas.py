from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_dto(cls, dto):
        return cls.model_validate(dto)

class IdMixinSchema:
    id: int

class TimeMixinSchema:
    created_at: datetime
