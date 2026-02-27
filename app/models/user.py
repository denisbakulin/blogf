from base.model import BaseORM, IdMixin, TimeMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Profile(BaseORM, IdMixin):
    __tablename__ = "profiles"

    bio: Mapped[str | None]
    age: Mapped[int | None]
    city: Mapped[str | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)



class Settings(BaseORM, IdMixin):
    __tablename__ = "user_settings"

    show_in_search: Mapped[bool] = mapped_column(default=True)

    is_profile_public: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)




class User(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    name: Mapped[str | None]
