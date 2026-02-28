from abac.access_level import AccessLevel
from abac.context import AccessContext
from DTO.container import ContainerDTO
from DTO.user import UserDTO


class AccessResolver:
    async def resolve(
            self, user: UserDTO,
            context: AccessContext,
            container: ContainerDTO,
    ) -> AccessLevel:

        if not user.is_active:
            return AccessLevel.BANNED

        if container.author_id == user.id:
            return AccessLevel.ADMIN

        if context.is_owner:
            return AccessLevel.OWNER


        return AccessLevel.NONE





