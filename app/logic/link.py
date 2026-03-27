from abac.container.policy import PrivateChannelPolicy
from entities import User

from services.container import AsyncSession

from services.channel import PrivateChannelService
from services.container_link import InviteLinkService
from services.join_request import JoinRequestService


__all__ = (
    "CreateInviteLinkUseCase",
    "CrossToInviteLinkUseCase",
    "GetInviteLinksUseCase"
)

class BaseLinkUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.session = session
        self.link = InviteLinkService(self.session)
        self.private = PrivateChannelService(self.session)
        self.policy = PrivateChannelPolicy

class CreateInviteLinkUseCase(BaseLinkUseCase):
    async def execute(self, user: User, channel_id: int):

        channel = await self.private.get_channel(channel_id)
        policy = self.policy(self.session, user=user, container=channel)

        await policy.ensure_is_admin()

        return await self.link.create_link(channel.id)


class GetInviteLinksUseCase(BaseLinkUseCase):
    async def execute(self, user: User, channel_id: int):
        channel = await self.private.get_channel(channel_id)
        policy = self.policy(self.session, user=user, container=channel)

        await policy.ensure_is_admin()

        return await self.link.repository.get_any_by(container_id=channel_id)


class CrossToInviteLinkUseCase(BaseLinkUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jr = JoinRequestService(self.session)

    async def execute(self, link: str, user: User):
        link = await self.link.get_by_or_raise(link=link)
        channel = await self.private.get_channel(link.container_id)

        #проверки хз короче потом придумаю дополнительно

        jr = await self.jr.create_jr(user_id=user.id, channel_id=channel.id)

        return jr

























