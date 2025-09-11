from user.schemas import UserShowMe, UserCreate
from pydantic import EmailStr, Field
from core.schemas import BaseSchema
from typing import Optional

class UserFields(BaseSchema):
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=True)
    is_admin: bool = Field(default=False)


class AdminUserShow(UserShowMe, UserFields):
    ...

class AdminUserCreate(UserCreate, UserFields):
    ...

class AdminUserUpdate(UserFields):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = None






from post.schemas import PostShow, PostBase


class AdminPostShow(PostShow):
    ...

class AdminPostCreate(PostBase):
    author_id: int


class AdminPostUpdate(PostBase):
    ...






