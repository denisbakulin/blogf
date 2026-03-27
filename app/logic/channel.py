from entities import Container,  User
from helpers.search import Pagination
from abac.container.policy import PrivateChannelPolicy
from services.container import ContainerService
from services.channel import PrivateChannelService
from services.subscribe import SubscribeService
from sqlalchemy.ext.asyncio import AsyncSession
from services.join_request import JoinRequestService
from base.exceptions import EntityBadRequestError


__all__ = (
    "GetPrivateChannelUseCase",
    "GetChannelSubscribersUseCase",
    "GetJRSUseCase",
    "ProcessJRSPUseCase",
)



class BaseChannelUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.container_service = ContainerService(session)

class BasePrivateChannelUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.policy = PrivateChannelPolicy
        self.service = PrivateChannelService(self.session)

class GetPrivateChannelUseCase(BasePrivateChannelUseCase):
    async def execute(self, user: User, channel_id: int) -> Container:

        channel = await self.service.get_channel(channel_id)

        policy = self.policy(session=self.session, user=user, channel=channel)

        await policy.ensure_read()

        return channel

class BaseJRSUseCase(BasePrivateChannelUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jr = JoinRequestService(self.session)

class GetJRSUseCase(BaseJRSUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jr = JoinRequestService(self.session)

    async def execute(self, user: User, channel_id: int):
        channel = await self.service.get_channel(channel_id)
        policy = self.policy(self.session, user=user, channel=channel)

        await policy.ensure_is_admin()

        return await self.jr.get_jrs(channel_id)


class ProcessJRSPUseCase(BaseJRSUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribe = SubscribeService(self.session)

    async def execute(self, user: User, jr_id: int, channel_id: int, accept: bool):
        channel = await self.service.get_channel(channel_id)
        jr = await self.jr.get_item_by_id(jr_id)

        if jr.channel_id != channel.id:
            raise EntityBadRequestError("Заявка не принадлежит этому каналу")

        policy = self.policy(self.session, user=user, channel=channel)

        await policy.ensure_is_admin()

        if accept:
            await self.subscribe.create_subscribe(
                user_id=jr.user_id, container_id=channel.id
            )
        await self.jr.delete_item_by_id(jr.id)




class GetChannelSubscribersUseCase(BaseChannelUseCase):
    async def execute(self, user_id: int, channel: Container, pagination: Pagination):
        if channel.author_id != user_id:
            raise EntityBadRequestError("Недостаточно прав")

        subs_service = SubscribeService(self.session)

        return await subs_service.get_container_subscribers(
            container_id=channel.id, pagination=pagination
        )






