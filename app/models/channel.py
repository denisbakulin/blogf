from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ContainerType(StrEnum):
    wall = "wall"
    topic = "topic"
    public_channel = "public_channel"
    private_channel = "private_channel"



class Container(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "containers"

    title: Mapped[str]
    slug: Mapped[str] = mapped_column(index=True, nullable=True)
    description: Mapped[str | None]
    type: Mapped[ContainerType]

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(
        "User", lazy="selectin"
    )







