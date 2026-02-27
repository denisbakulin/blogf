from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Post(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    content: Mapped[str] = mapped_column(nullable=False)

    allow_comments: Mapped[bool] = mapped_column(default=True)
    allow_reactions: Mapped[bool] = mapped_column(default=True)

    container_id: Mapped[int] = mapped_column(ForeignKey("containers.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship("User", lazy="selectin")
    container: Mapped["Container"] = relationship("Container", lazy="selectin")
