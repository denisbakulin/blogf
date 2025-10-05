from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdMixinSchema:
    id: int


class TimeMixinSchema:
    created_at: datetime
