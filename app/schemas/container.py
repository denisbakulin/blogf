from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from entities.container import ContainerType


class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType

class ContainerUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None

class WallShow(BaseSchema, TimeMixinSchema):
    title: str | None
