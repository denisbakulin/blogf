from core.schemas import BaseSchema


class LoginTokens(BaseSchema):
    access_token: str
    refresh_token: str


class TokenInfo(BaseSchema):
    type: str
    user_id: int

class AuthCreds(BaseSchema):
    username: str
    password: str

