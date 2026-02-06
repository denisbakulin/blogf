from sqlalchemy.orm import Mapped, mapped_column

from base.model import BaseORM, IdMixin


class TgVerified(BaseORM, IdMixin):

    __tablename__ = "tg_ids"
    tg_id: Mapped[int] = mapped_column(unique=True)



from sqlalchemy.ext.asyncio import AsyncSession
from base.repository import BaseRepository


class TgVerifiedRepository(BaseRepository[TgVerified]):

    def __init__(self, session: AsyncSession):
        super().__init__(TgVerified, session)



from base.service import BaseService
class TgVerifiedService(BaseService[TgVerified, TgVerifiedRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(TgVerified, session, TgVerifiedRepository)


from typing import Annotated
from fastapi import Depends
from base.db import get_session

async def get_tgver_service(
        session: AsyncSession = Depends(get_session)
) -> TgVerifiedService:
    return TgVerifiedService(session=session)


tgvServiceDep = Annotated[TgVerifiedService, Depends(get_tgver_service)]
