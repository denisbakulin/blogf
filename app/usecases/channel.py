from base.exceptions import EntityBadRequestError

from entities import Container, ContainerType
from helpers.search import Pagination
from schemas.admin import AdminCreate

from schemas.channel import ChannelCreate
from services.admin import AdminService
from services.container import ContainerService

from services.subscribe import SubscribeService
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService
from utils.post import generate_slug


channels = [
    ContainerType.PUBLIC_CHANNEL,
    ContainerType.PRIVATE_CHANEL,
]

class BaseChannelUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.container_service = ContainerService(session)


class CreateChannelUseCase(BaseChannelUseCase):
    async def execute(self, user_id: int, create: ChannelCreate):
        await self.container_service.check_already_exists(
            slug=create.slug, type=channels
        )

        create.slug = generate_slug(create.slug)

        return await self.container_service.create_item(
            author_id=user_id, **create.dict(),
            type=channels[create.is_private]
        )


class GetChannelSubscribersUseCase(BaseChannelUseCase):
    async def execute(self, user_id: int, channel: Container, pagination: Pagination):
        if channel.author_id != user_id:
            raise EntityBadRequestError("Недостаточно прав")

        subs_service = SubscribeService(self.session)

        return await subs_service.get_container_subscribers(
            container_id=channel.id, pagination=pagination
        )


class SetChannelAdminUseCase(BaseChannelUseCase):
    async def execute(self, user_id: int, admin: AdminCreate, channel: Container):
        admin_service = AdminService(self.session)
        user_service = UserService(self.session)

        if channel.author_id != user_id:
            raise EntityBadRequestError("Недостаточно прав")

        user = await user_service.get_user_by_username(admin.username)

        await admin_service.create_admin(
            user_id=user.id, container_id=channel.id
        )




