from abac.access_level import AccessLevel
from abac.context import ContextResolver
from abac.policy import BasePolicy
from services.subscribe import SubscribeService

from entities.user import User
from entities.post import Post
from entities.container import Container


class ChannelPolicy:

    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service


    def ensure_is_admin(self, user: User, container: Container):
        BasePolicy._ensure(user.id == container.author_id)

    def ensure_update(self, user: User, container: Container):
        self.ensure_is_admin(user, container)

    def ensure_delete(self, user: User, container: Container):
        self.ensure_is_admin(user,container)


class PrivateChannelPolicy(ChannelPolicy):
    def get_jrs(self, user: User, container: Container):
        self.ensure_is_admin(user, container)







