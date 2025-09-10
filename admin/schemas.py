from user.schemas import UserShowMe, UserUpdate, UserProfile, UserCreate
from pydantic import EmailStr, BaseModel
from core.schemas import BaseSchema

class UserFields(BaseSchema):
    is_active: bool
    is_verified: bool

class AdminUserShow(UserShowMe, UserFields):
    is_admin: bool


class AdminUserUpdate(UserFields):
    username: str
    email: EmailStr


class AdminUserCreate(UserCreate, UserFields):
    ...






