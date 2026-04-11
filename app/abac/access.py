from abac.access_level import AccessLevel
from abac.data import AccessContext
from entities.container import Container
from entities.user import User


class AccessResolver:

    @staticmethod
    def resolve(
        user: User,
        context: AccessContext,
        container: Container,
    ) -> AccessLevel:

        if not user.is_active:
            return AccessLevel.BANNED

        if container.author_id == user.id:
            return AccessLevel.CONTAINER_OWNER

        if context.is_owner:
            return AccessLevel.ENTITY_OWNER


        return AccessLevel.UNDEFINED





