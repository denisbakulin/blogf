from enum import StrEnum

from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class NotificationType(StrEnum):
    BASE_LOGIN = "BASE_LOGIN"
    NEW_POST = "NEW_POST"


class Notification(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "user_notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[NotificationType]











