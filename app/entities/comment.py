from base.model import BaseORM, TimeMixin, OwnedByUserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Comment(BaseORM, TimeMixin, OwnedByUserMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)






