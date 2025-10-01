from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin


class Post(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    slug: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)

    author: Mapped["User"] = relationship("User", back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
