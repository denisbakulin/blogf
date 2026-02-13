from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from join_request.model import JoinRequest


class JoinRequestRepository(BaseRepository[JoinRequest]):

    def __init__(self, session: AsyncSession):
        super().__init__(JoinRequest, session)







