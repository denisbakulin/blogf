from enum import StrEnum, auto

from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ContainerType(StrEnum):
    WALL = auto()
    TOPIC = auto()
    PUBLIC_CHANNEL = auto()
    PRIVATE_CHANEL = auto()


class Container(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "containers"

    title: Mapped[str]
    slug: Mapped[str | None] = mapped_column(index=True, nullable=True)
    description: Mapped[str | None]
    type: Mapped[ContainerType]

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))











