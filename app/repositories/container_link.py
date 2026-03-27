from base.repository import BaseRepository
from entities import InviteLink

from sqlalchemy.ext.asyncio import AsyncSession


class InviteLinkRepository(BaseRepository[InviteLink]):
    def __init__(self, session: AsyncSession):
        super().__init__(InviteLink, session)









