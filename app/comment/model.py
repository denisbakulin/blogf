from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.model import BaseORM, TimeMixin


class Comment(BaseORM, TimeMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    content: Mapped[str] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


    post: Mapped["Post"] = relationship("Post", lazy="joined")
    author: Mapped["User"] = relationship("User", lazy="joined", foreign_keys=[author_id])
    user: Mapped["User"] = relationship("User", lazy="joined", foreign_keys=[user_id])


    parent: Mapped["Comment"] = relationship(
        "Comment",
        remote_side=[id]
    )





