from enum import StrEnum, auto

from base.model import BaseORM, IdMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AllowAction(StrEnum):
    CREATE = auto()
    EDIT = auto()
    DELETE = auto()
    READ = auto()

class AllowEntity(StrEnum):
    USER = auto()
    CONTAINER = auto()
    POST = auto()
    COMMENT = auto()
    REACTION = auto()
    TOPIC_OFFER = auto()

class Allow(BaseORM, IdMixin):
    __tablename__ = "user_allows"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[AllowAction]
    entity: Mapped[AllowEntity]

    context: Mapped[AllowEntity | None]
    context_id: Mapped[int | None]

