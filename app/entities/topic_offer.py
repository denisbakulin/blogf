from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class TopicOfferStatus(StrEnum):
    PENDING = "pending"
    APPROVE = "approve"
    REJECT = "reject"



class TopicOffer(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topic_offers"

    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TopicOfferStatus] = mapped_column(default=TopicOfferStatus.PENDING)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    process_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    release_topic_id: Mapped[int | None] = mapped_column(ForeignKey("containers.id"), nullable=True)










