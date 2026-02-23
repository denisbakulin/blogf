from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from container.model import ContainerType
from user.schemas import ShortUserInfo


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

