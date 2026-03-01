from typing import Annotated

from base.db import get_session
from base.model import BaseORM, IdMixin
from base.repository import BaseRepository
from base.service import BaseService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class TgVerified(BaseORM, IdMixin):

    __tablename__ = "tg_ids"
    tg_id: Mapped[int] = mapped_column(unique=True)




class TgVerifiedRepository(BaseRepository[TgVerified]):

    def __init__(self, session: AsyncSession):
        super().__init__(TgVerified, session)





class TgVerifiedService(BaseService[TgVerified, TgVerifiedRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(TgVerified, session, TgVerifiedRepository)




async def get_tgver_service(
        session: AsyncSession = Depends(get_session)
) -> TgVerifiedService:
    return TgVerifiedService(session=session)


tgvServiceDep = Annotated[TgVerifiedService, Depends(get_tgver_service)]
