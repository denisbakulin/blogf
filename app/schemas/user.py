from typing import Annotated

from base.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema
from pydantic import Field


class UserProfile(BaseSchema):
    bio: Annotated[str | None, Field(default=None, max_length=500)] = None
    age: Annotated[int | None, Field(default=None, ge=0, le=120)] = None
    city: Annotated[str | None, Field(default=None, max_length=100)] = None

class UserSettings(BaseSchema):
    show_in_search: bool
    is_profile_public: bool


class UserUsername(BaseSchema, IdMixinSchema):
    username: str



class UserCreate(BaseSchema):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=5, max_length=72)




class UserUpdate(BaseSchema):
    username: str | None = None
    name: str | None = None
    profile: UserProfile | None = None





class UserShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    username: str
    name: str | None
    is_active: bool
    is_verified: bool


class UserProfileShow(BaseSchema):
    user: UserShow
    profile: UserProfile








