from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from entities.container import ContainerType
from schemas.user import UserUsername


class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType


class ContainerSlug(BaseSchema):
    slug: str



class FullContainerShow(BaseSchema):
    container: ContainerShow
    post_count: int
    comment_count: int

