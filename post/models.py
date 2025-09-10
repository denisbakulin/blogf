from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models import BaseORM
from sqlalchemy import ForeignKey
from datetime import datetime


class Post(BaseORM):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    slug: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    author: Mapped["User"] = relationship("User", back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post"
    )

