from base.model import BaseORM, TimeMixin, IdMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class PinnedPost(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "pinned_posts"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    order_id: Mapped[int]







