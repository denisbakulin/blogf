from dataclasses import dataclass
from urllib import parse

from auth.oauth import OAuthUserService, ProviderType
from auth.user_create import UserCreator
from base.settings import google_oauth_settings
from exceptions.auth import AuthError
from httpx import AsyncClient
from jose import jwt
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_fixed
from utils.auth import TokenCreator

GOOGLE_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@dataclass
class GoogleUserCreds:
    google_id: str
    name: str


@dataclass
class GoogleTokenInfo:
    access: str
    token: str



def decode_google_token(token: str, access_token: str) -> GoogleUserCreds:
    decoded = jwt.decode(
        token, key="",
        options={
            "verify_signature": False,  # Отключает проверку подписи
            "verify_aud": False,
            "verify_iat": False,
            "verify_exp": False
        },
        access_token=access_token
    )
    name = decoded.get("name")
    google_id = decoded.get("sub")

    return GoogleUserCreds(
        name=name,
        google_id=google_id
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(4))
async def get_google_token(code: str) -> GoogleTokenInfo:
    async with AsyncClient() as client:
        response = await client.post(
            url=GOOGLE_TOKEN_URL,
            data={
                "client_id": google_oauth_settings.client_id,
                "client_secret": google_oauth_settings.client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:5173/auth/google/login",
                "code": code
            }
        )

        result = response.json()
        token = result.get("id_token")
        access_token = result.get("access_token")

        if not token or not access_token:
            raise AuthError("истекший токерн")

        return GoogleTokenInfo(token=token, access=access_token)



class GoogleAuth:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_s = UserService(session)
        self.user_creator = UserCreator(session)
        self.oauth = OAuthUserService(session)


    @property
    def oauth_uri(self):
        params = {
            "client_id": google_oauth_settings.client_id,
            "redirect_uri": "http://localhost:5173/auth/google/login",
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "profile"
            ])
        }
        string = parse.urlencode(params, quote_via=parse.quote)

        return f"{GOOGLE_BASE_URL}?{string}"


    async def login(self, code: str):

        tokens = await get_google_token(code)
        creds = decode_google_token(tokens.token, tokens.access)

        google_user = await self.oauth.repository.get_one_by(
            provider=ProviderType.GOOGLE, provider_id=creds.google_id
        )

        if google_user:
            return TokenCreator(google_user.user_id).auth_tokens

        user = await self.user_creator.execute(creds.name)

        await self.oauth.create_item(
            user_id=user.id, provider=ProviderType.GOOGLE, provider_id=creds.google_id
        )

        return TokenCreator(user.id).auth_tokens


