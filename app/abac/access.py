from abac.access_level import AccessLevel
from abac.data import AccessContext


from entities.user import User
from entities.container import Container

class AccessResolver:
    async def resolve(
            self, user: User,
            context: AccessContext,
            container: Container,
    ) -> AccessLevel:

        if not user.is_active:
            return AccessLevel.BANNED

        if container.author_id == user.id:
            return AccessLevel.ADMIN

        if context.is_owner:
            return AccessLevel.OWNER


        return AccessLevel.NONE





