from typing import Annotated

from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from pydantic import Field, field_serializer, field_validator
from user.model import UserRoleEnum


class ShortUserInfo(BaseSchema, IdMixinSchema):
    username: str
    name: str | None


class UserCreate(BaseSchema):
    username: str = Field(min_length=1)
    password: str = Field(min_length=5)

    @field_validator("username")
    def normalize_name(cls, username: str):
        return username.strip().lower()


class UserProfile(BaseSchema):
    bio: Annotated[str | None, Field(default=None, max_length=500)] = None
    age: Annotated[int | None, Field(default=None, ge=0, le=120)] = None
    city: Annotated[str | None, Field(default=None, max_length=100)] = None
    foreign_link: Annotated[str | None, Field(default=None, max_length=255)] = None


class UserUpdate(BaseSchema):
    username: str | None = None
    name: str | None = None
    profile: UserProfile | None = None


class UserShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    username: str
    profile: UserProfile
    is_active: bool
    is_verified: bool
    name: str | None


class UserShowMe(UserShow):
    role: UserRoleEnum


    @field_serializer("role")
    def role_serialize(self, role: UserRoleEnum):
        return role._name_



class PasswordChange(BaseSchema):

    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)



class UserSettings(BaseSchema):

    show_in_search: bool

    direct_notifications: bool
    reaction_notifications: bool
    comment_notifications: bool

    enable_direct: bool
    is_profile_public: bool


