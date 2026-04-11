from entities import User
from services.allow import AllowService
from schemas.allow import AllowCreate

from services.container import AsyncSession, ContainerService
from abac.context_resolver import ContextResolver, AccessLevel
from abac.policy import ContextEnsure

from services.user import UserService

__all__ = (
    "CreateContainerAllowUseCase",
)




class BaseAllowUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.allow_service = AllowService(self.session)
        self.user_service = UserService(self.session)
        self.container_service = ContainerService(self.session)
        self.policy = ContextResolver(self.session)


class CreateContainerAllowUseCase(BaseAllowUseCase):

    async def execute(self, admin: User, allow: AllowCreate):
        user = await self.user_service.get_user_by_id(allow.user_id)
        container = await self.container_service.get_item_by_id(allow.container_id)

        #Тока админы канала могут назначать права
        admin_ctx = await self.policy.resolve(user=admin, container=container)
        ContextEnsure(admin_ctx).ge_role(AccessLevel.ADMIN)

        #Пользователь является участником контейнера
        user_ctx = await self.policy.resolve(user=user, container=container)
        ContextEnsure(user_ctx).ge_role(AccessLevel.VIEWER)


        return await self.allow_service.create_allow(
            **allow.model_dump()
        )














