from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from base.model import BaseORM, IdMixin, TimeMixin


class NotificationType(StrEnum):
    BASE_LOGIN = "BASE_LOGIN"
    NEW_POST = "NEW_POST"


class Notification(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "user_notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[NotificationType]

    #лень делать говно поотом











