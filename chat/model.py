from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, TimeMixin, IdMixin

class BaseMessage(BaseORM, TimeMixin, IdMixin):
    __abstract__ = True

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(nullable=False)





class DirectMessage(BaseMessage):
    __tablename__ = "direct_messages"

    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))



class GeneralMessage(BaseMessage):
    __tablename__ = "general_messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey("general_chats.id"))



class GeneralChat(BaseORM, IdMixin):
    __tablename__ = "general_chats"

    private: Mapped[bool] = mapped_column(default=True)



class GeneralChatMembers(BaseORM, TimeMixin):
    __tablename__ = "general_chat_members"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("general_chats.id"), primary_key=True)



class DirectChat(BaseORM, TimeMixin):
    __tablename__ = "direct_chats"

    first_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    second_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    banned_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    first_user = relationship(
        "User",
        foreign_keys=[first_user_id],
    )


    second_user = relationship(
        "User",
        foreign_keys=[second_user_id],
    )

    def __repr__(self):
        return f"Личный чат [{self.first_user.username} - {self.second_user.username}]"








