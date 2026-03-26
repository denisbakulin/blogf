from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin, UpdatedAtMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Post(BaseORM, IdMixin, TimeMixin, OwnedByUserMixin, UpdatedAtMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    content: Mapped[str] = mapped_column(nullable=False)

    allow_comments: Mapped[bool] = mapped_column(default=True)
    allow_reactions: Mapped[bool] = mapped_column(default=True)

    container_id: Mapped[int] = mapped_column(ForeignKey("containers.id"))
