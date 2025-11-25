from pydantic import BaseModel


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


