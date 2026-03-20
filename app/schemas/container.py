from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from entities  import ContainerType


class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType

class ContainerMetricsShow(ContainerShow):
    post_count: int
    comment_count: int

class ContainerUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None

class WallShow(BaseSchema, TimeMixinSchema):
    title: str | None


