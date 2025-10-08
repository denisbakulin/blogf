from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin


class Profile(BaseORM, IdMixin):
    __tablename__ = "profiles"

    bio: Mapped[str | None]
    avatar: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    foreign_link: Mapped[str | None]

    user: Mapped["User"] = relationship(back_populates="profile")


class Settings(BaseORM, IdMixin):
    __tablename__ = "user_settings"

    show_in_search: Mapped[bool] = mapped_column(default=True)

    direct_notifications: Mapped[bool] = mapped_column(default=True)
    reaction_notifications: Mapped[bool] = mapped_column(default=True)
    comment_notifications: Mapped[bool] = mapped_column(default=True)


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="settings")




class User(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "users"

    depends = [("profile", Profile), ("settings", Settings)]

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    settings: Mapped["Settings"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )



