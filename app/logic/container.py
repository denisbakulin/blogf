from typing import Literal

from abac.container.policy import BaseContainerPolicy
from entities import User
from schemas.admin import AdminCreate
from schemas.container import ContainerUpdate, ContainerType
from services.admin import AdminService
from services.container import AsyncSession, ContainerService

from services.user import UserService

from base.exceptions import LogicError

__all__ = (
    "UpdateContainerUseCase",
    "UpdateWallUseCase",
    "ProcessContainerAdminUseCase"
)




class BaseContainerUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.container_service = ContainerService(session)
        self.policy = BaseContainerPolicy
        self.session = session



class UpdateContainerUseCase(BaseContainerUseCase):
    async def execute(self, user: User, container_id: int, update: ContainerUpdate):
        container = await self.container_service.get_item_by_id(container_id)

        policy = self.policy(self.session, user=user, container=container)

        await policy.ensure_is_admin()

        return await self.container_service.update_container(
            container_id=container_id, update=update
        )

class UpdateWallUseCase(BaseContainerUseCase):
    async def execute(self, user: User, update: ContainerUpdate):
        container = await self.container_service.get_by_or_raise(
            author_id=user.id, type=ContainerType.WALL
        )
        policy = self.policy(self.session, user=user, container=container)

        await policy.ensure_is_admin()

        await self.container_service.update_container(
            container_id=container.id, update=update
        )



class ProcessContainerAdminUseCase(BaseContainerUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_service = AdminService(self.session)
        self.user_service = UserService(self.session)


    async def execute(self, user: User, admin: AdminCreate, method: Literal["create", "delete"]):
        admin_user = await self.user_service.get_user_by_id(admin.user_id)
        container = await self.container_service.get_item_by_id(admin.container_id)

        policy = self.policy(self.session, user=user, container=container)

        await policy.ensure_is_owner()

        match method:
            case "create":
                await self.admin_service.create_admin(
                    user_id=admin_user.id, container_id=container.id
                )
            case "delete":
                adm_column = await self.admin_service.get_by_or_raise(
                    user_id=admin_user.id, container_id=container.id
                )
                await self.admin_service.delete_item_by_id(
                    adm_column.id
                )

            case _:
                raise LogicError("Некорректное Действие")



















