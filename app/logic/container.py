from abac.container.policy import BaseContainerPolicy
from base.exceptions import EntityBadRequestError
from entities import User, Container
from schemas.admin import AdminCreate
from schemas.container import ContainerUpdate, ContainerType
from services.admin import AdminService
from services.channel import PrivateChannelService, PublicChannelService
from services.container import AsyncSession, ContainerService
from services.topic import TopicService
from services.user import UserService

__all__ = (
    "UpdateContainerUseCase",
    "UpdateWallUseCase",
    "get_container_by_identifier",
    "SetContainerAdminUseCase"
)




async def get_container_by_identifier(
    ctype: ContainerType,
    value: str,
    session: AsyncSession
) -> Container:
    match ctype:
        case ContainerType.PRIVATE_CHANEL if value.isdigit():
            service = PrivateChannelService(session)
            channel_value = int(value)

        case ContainerType.PUBLIC_CHANNEL:
            service = PublicChannelService(session)
            channel_value = value

        case ContainerType.TOPIC if value.isdigit():
            return await TopicService(session).get_topic(
                topic_id=int(value)
            )
        case _:
            raise EntityBadRequestError(ctype)

    return await service.get_channel(channel_value)


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



class SetContainerAdminUseCase(BaseContainerUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_service = AdminService(self.session)
        self.user_service = UserService(self.session)

    async def execute(self, user: User, admin: AdminCreate, container: Container):
        admin = await self.user_service.get_user_by_username(admin.username)

        policy = self.policy(self.session, user=user, container=container)

        await policy.ensure_is_admin()

        await self.admin_service.create_admin(
            user_id=admin.id, container_id=container.id
        )



















