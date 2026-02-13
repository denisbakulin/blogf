from enum import IntEnum

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.model import BaseORM, IdMixin, TimeMixin


class UserRoleEnum(IntEnum):
    SUPER_ADMIN = 5
    ADMIN = 4
    MODERATOR = 3
    USER = 2
    ANONYMOUS = 1


class Profile(BaseORM, IdMixin):
    __tablename__ = "profiles"

    bio: Mapped[str | None]
    age: Mapped[int | None]
    city: Mapped[str | None]


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="profile")


class Settings(BaseORM, IdMixin):
    __tablename__ = "user_settings"

    show_in_search: Mapped[bool] = mapped_column(default=True)

    direct_notifications: Mapped[bool] = mapped_column(default=True)
    reaction_notifications: Mapped[bool] = mapped_column(default=True)
    comment_notifications: Mapped[bool] = mapped_column(default=True)
    subscribe_notifications: Mapped[bool] = mapped_column(default=True)

    is_profile_public: Mapped[bool] = mapped_column(default=True)
    enable_direct: Mapped[bool] = mapped_column(default=True)


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="settings")




class User(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "users"

    depends = [("profile", Profile), ("settings", Settings)]

    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.USER)
    name: Mapped[str | None]

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



