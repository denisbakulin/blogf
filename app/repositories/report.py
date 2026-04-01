from base.repository import BaseRepository

from entities import Report
from sqlalchemy.ext.asyncio import AsyncSession


class ReportRepository(BaseRepository[Report]):

    def __init__(self, session: AsyncSession):
        super().__init__(Report, session)







