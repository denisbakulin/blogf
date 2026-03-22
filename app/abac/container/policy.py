from abac.policy import  ContextEnsure
from entities.container import Container
from entities.user import User



class BaseContainerPolicy:
    def ensure_is_admin(self, user: User, container: Container):
        ContextEnsure._ensure(user.id == container.author_id, "Не админ")

    def ensure_update(self, user: User, container: Container):
        self.ensure_is_admin(user, container)

    def ensure_delete(self, user: User, container: Container):
        self.ensure_is_admin(user, container)


class PrivateChannelPolicy(BaseContainerPolicy):
    def get_jrs(self, user: User, container: Container):
        self.ensure_is_admin(user, container)







