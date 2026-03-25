from abac.container.policy import BaseContainerPolicy
from entities import User
from schemas.container import ContainerUpdate, ContainerType
from services.container import AsyncSession, ContainerService


class BaseContainerUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.container_service = ContainerService(session)
        self.policy = BaseContainerPolicy()



class UpdateContainerUseCase(BaseContainerUseCase):
    async def execute(self, user: User, container_id: int, update: ContainerUpdate):
        container = await self.container_service.get_item_by_id(container_id)

        self.policy.ensure_update(user=user, container=container)

        return await self.container_service.update_container(
            container_id=container_id, update=update
        )

class UpdateWallUseCase(BaseContainerUseCase):
    async def execute(self, user: User, update: ContainerUpdate):
        container = await self.container_service.get_by_or_raise(
            author_id=user.id, type=ContainerType.WALL
        )
        self.policy.ensure_update(user=user, container=container)

        await self.container_service.update_container(
            container_id=container.id, update=update
        )






















