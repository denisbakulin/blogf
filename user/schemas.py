from typing import Optional

from pydantic import EmailStr, Field, field_validator

from core.schemas import BaseSchema,  IdMixinSchema, TimeMixinSchema




class UserCreate(BaseSchema):
    username: str = Field(min_length=1)
    password: str = Field(min_length=5)
    email: EmailStr | None = None

    bio: str | None = None
    avatar: str | None = None


    @field_validator("username")
    def normalize_name(cls, username: str):
        return username.strip().lower()


class UserUpdate(BaseSchema):
    bio: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    avatar: Optional[str] = Field(default=None)


class UserProfile(BaseSchema):
    bio: str | None = None
    avatar: str | None = None


class UserShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    username: str
    profile: UserProfile | None
    is_active: bool


class UserShowMe(UserShow):
    email: str
    is_verified: bool
    is_admin: bool



class PasswordChange(BaseSchema):

    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)

class EmailUpdate(BaseSchema):
    new_email: EmailStr


class UserSettings(BaseSchema):

    show_in_search: bool

