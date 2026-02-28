from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from models.container import ContainerType


class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType

    author_username: str

class ContainerSlug(BaseSchema):
    slug: str



class FullContainerShow(BaseSchema):
    container: ContainerShow
    post_count: int
    comment_count: int

