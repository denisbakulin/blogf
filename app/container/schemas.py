from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from user.schemas import UserUsername
from container.model import ContainerType

class ContainerShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    title: str
    slug: str
    description: str
    type: ContainerType

    author: UserUsername



class FullContainerShow(BaseSchema):
    container: ContainerShow
    post_count: int
    comment_count: int

