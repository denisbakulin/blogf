from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from typing import Literal
from user.schemas import ShortUserInfo
from container.schemas import ContainerShow


class ContainerSubs(BaseSchema):
    topics: list[ContainerShow]
    private_channels: list[ContainerShow]
    public_channels: list[ContainerShow]

class ListOfSubscribes(BaseSchema):
    creator_subs: list[ShortUserInfo]
    container_subs: ContainerSubs



class SubscribeBase(BaseSchema, IdMixinSchema, TimeMixinSchema):
    user: ShortUserInfo

class SubscriberOfContainerShow(SubscribeBase):
    container: ContainerShow

class SubscribeOfUserShow(SubscribeBase):
    creator: ShortUserInfo


subscribe_type = Literal["user", "topic", "channel"]






