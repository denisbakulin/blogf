import datetime

from pydantic import EmailStr, Field, field_validator
from core.schemas import BaseSchema



class UserCreate(BaseSchema):
    username: str = Field(min_length=1)
    password: str = Field(min_length=5)
    email: EmailStr | None = None

    @field_validator("username")
    def normalize_name(cls, username: str):
        return username.strip().lower()


class UserUpdate(BaseSchema):
    bio: str | None = None
    username: str = None
    avatar: str | None


class UserProfile(BaseSchema):
    bio: str | None = None
    avatar: str | None = None


class UserShow(BaseSchema):
    id: int
    username: str
    profile: UserProfile | None
    created_at:  datetime.datetime


class UserShowMe(UserShow):
    email: str





class PasswordChange(BaseSchema):

    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)

class EmailUpdate(BaseSchema):
    new_email: EmailStr
