from base.service import BaseService
from entities import InviteLink
from repositories import InviteLinkRepository
from utils.user import create_username
from sqlalchemy.ext.asyncio import AsyncSession


class InviteLinkService(BaseService[InviteLink, InviteLinkRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(InviteLink, session, InviteLinkRepository)


    async def create_link(self, container_id: int) -> InviteLink:
        link = create_username(15)

        return await self.create_item(
            container_id=container_id, link=link
        )






