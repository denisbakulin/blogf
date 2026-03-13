from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin
from base.repository import BaseRepository
from base.service import BaseService
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class ProviderType(StrEnum):
    TELEGRAM = "TELEGRAM"
    GOOGLE = "GOOGLE"
    GITHUB = "GITHUB"



class OAuthUser(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "oauth_users"

    provider_id: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[ProviderType]



class OAuthUserRepository(BaseRepository[OAuthUser]):

    def __init__(self, session: AsyncSession):
        super().__init__(OAuthUser, session)


class OAuthUserService(BaseService[OAuthUser, OAuthUserRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(OAuthUser, session, OAuthUserRepository)


