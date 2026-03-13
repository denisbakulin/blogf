from pydantic import BaseModel, Field


class AccessTokenResponse(BaseModel):
    access_token: str


class LoginTokens(BaseModel):
    access: str
    refresh: str


class TokenInfo(BaseModel):
    type: str
    user_id: int


class AuthCreds(BaseModel):
    username: str = "admin"
    password: str = "admin"


class PasswordChange(BaseModel):
    old_password: str | None = Field(min_length=5, default=None)
    new_password: str = Field(min_length=5, max_length=72)


class ResetPassword(BaseModel):
    password: str = Field(min_length=5, max_length=72)

class ForgetPassword(BaseModel):
    username: str

class LoginTelegram(BaseModel):
    token: str
    name: str

class LoginGoogle(BaseModel):
    code: str
