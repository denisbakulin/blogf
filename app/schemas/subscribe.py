
from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from schemas.container import ContainerShow
from schemas.user import UserUsername


class ContainerSubs(BaseSchema):
    topics: list[ContainerShow]
    private_channels: list[ContainerShow]
    public_channels: list[ContainerShow]


class ListOfSubscribes(BaseSchema):
    creator_subs: list[UserUsername]
    container_subs: ContainerSubs



class SubscribeBase(BaseSchema, IdMixinSchema, TimeMixinSchema):
    user: UserUsername

class SubscriberOfContainerShow(SubscribeBase):
    container: ContainerShow








