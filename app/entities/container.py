from enum import StrEnum, auto

from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin
from sqlalchemy.orm import Mapped, mapped_column


class ContainerType(StrEnum):
    WALL = auto()
    TOPIC = auto()
    PUBLIC_CHANNEL = auto()
    PRIVATE_CHANEL = auto()


class Container(BaseORM, IdMixin, TimeMixin, OwnedByUserMixin):
    __tablename__ = "containers"

    title: Mapped[str]
    slug: Mapped[str | None] = mapped_column(index=True, nullable=True)
    description: Mapped[str | None]
    type: Mapped[ContainerType]

    post_count: Mapped[int] = mapped_column(default=0)
    comment_count: Mapped[int] = mapped_column(default=0)













