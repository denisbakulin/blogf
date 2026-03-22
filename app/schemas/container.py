from base.schemas import BaseSchema,  TimeMixinSchema
from entities  import ContainerType


class ContainerShow(BaseSchema, TimeMixinSchema):
    title: str | None
    slug: str | None
    description: str | None
    type: ContainerType

class ContainerMetricsShow(ContainerShow):
    post_count: int
    comment_count: int

class ContainerUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None

class WallShow(BaseSchema, TimeMixinSchema):
    title: str | None


