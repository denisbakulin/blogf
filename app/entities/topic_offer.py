from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin, OwnedByUserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class TopicOfferStatus(StrEnum):
    PENDING = "pending"
    APPROVE = "approve"
    REJECT = "reject"



class TopicOffer(BaseORM, IdMixin, TimeMixin, OwnedByUserMixin):
    __tablename__ = "topic_offers"

    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TopicOfferStatus] = mapped_column(default=TopicOfferStatus.PENDING)

    process_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    release_topic_id: Mapped[int | None] = mapped_column(ForeignKey("containers.id"), nullable=True)










