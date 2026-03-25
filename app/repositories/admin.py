from sqlalchemy.ext.asyncio import AsyncSession

from entities import Admin
from base.repository import BaseRepository


class AdminRepository(BaseRepository[Admin]):

    def __init__(self, session: AsyncSession):
        super().__init__(Admin, session)


