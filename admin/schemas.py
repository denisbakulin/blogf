from typing import Optional

from pydantic import EmailStr, Field

from core.schemas import BaseSchema
from user.schemas import UserCreate, UserShowMe


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






from post.schemas import PostBase, PostShow


class AdminPostShow(PostShow):
    ...






