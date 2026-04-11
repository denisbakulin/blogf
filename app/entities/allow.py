from enum import StrEnum, auto

from base.model import BaseORM, IdMixin, DBEntity
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class AllowAction(StrEnum):
    CREATE = auto()
    EDIT = auto()
    DELETE = auto()
    READ = auto()


class Allow(BaseORM, IdMixin):
    __tablename__ = "user_allows"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[AllowAction]
    entity: Mapped[DBEntity]

    container_id: Mapped[int | None]

    against: Mapped[bool] = mapped_column(default=False)


