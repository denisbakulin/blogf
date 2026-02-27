from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from models.container import ContainerType
from schemas.user import ShortUserInfo


class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType

    author: ShortUserInfo



class FullContainerShow(BaseSchema):
    container: ContainerShow
    post_count: int
    comment_count: int

