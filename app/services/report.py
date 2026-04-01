from base.service import BaseService
from entities import Report
from repositories import ReportRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ReportService(BaseService[Report, ReportRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Report, session, ReportRepository)


