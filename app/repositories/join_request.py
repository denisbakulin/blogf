from base.repository import BaseRepository
from models.join_request import JoinRequest
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.join_request import JoinRequestDTO

class JoinRequestRepository(BaseRepository[JoinRequest, JoinRequestDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(JoinRequest, session, JoinRequestRepository)









