from pydantic import BaseModel, Field



class AccessTokenResponse(BaseModel):
    access_token: str


class LoginTokens(BaseModel):
    access: str
    refresh: str

class TgLoginAnswer(LoginTokens):
    success_verify: bool



class TokenInfo(BaseModel):
    type: str
    user_id: int


class AuthCreds(BaseModel):
    username: str = "admin"
    password: str = "admin"

class TgAuthCode(BaseModel):
    code: str

class PasswordChange(BaseModel):
    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5, max_length=72)



class ForgetPassword(BaseModel):
    username: str

