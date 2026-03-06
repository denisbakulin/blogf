from sqlalchemy.ext.asyncio import AsyncSession
from base.settings import google_oauth_settings
from urllib import parse
from utils.auth import LoginTokens, TokenCreator, generate_auth_code
from services.user import UserService
from httpx import AsyncClient
from auth.user_create import UserCreator
from auth.oauth import OAuthUserService, ProviderType
from exceptions.auth import AuthError


class GoogleAuth:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_s = UserService(session)
        self.user_creator = UserCreator(session)
        self.oauth = OAuthUserService(session)
        self.base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.certs_url = "https://www.googleapis.com/oauth2/v3/certs"


    @property
    def oauth_uri(self):
        params = {
            "client_id": google_oauth_settings.client_id,
            "redirect_uri": "http://localhost:8000/auth/google/login",
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "profile"
            ])
        }
        string = parse.urlencode(params, quote_via=parse.quote)

        return f"{self.base_url}?{string}"

    async def login(self, code: str):
        from jose import jwt


        async with AsyncClient() as client:
            response = await client.post(
                url=self.token_url,
                data={
                    "client_id": google_oauth_settings.client_id,
                    "client_secret": google_oauth_settings.client_secret,
                    "grant_type": "authorization_code",
                    "redirect_uri": "http://localhost:8000/auth/google/login",
                    "code": code
                }
            )

            result = response.json()
            token = result.get("id_token")
            access_token = result.get("access_token")
            if not token or not access_token:
                raise AuthError("истекший токерн")
            
            payload = jwt.decode(
                token,
                key="",
                options={
                    "verify_signature": False,  # Отключает проверку подписи
                    "verify_aud": False,
                    "verify_iat": False,
                    "verify_exp": False
                },
                access_token=access_token
            )
            name = payload.get("name")
            google_id = payload.get("sub")

            google_user = await self.oauth.repository.get_one_by(
                provider=ProviderType.GOOGLE, provider_id=google_id
            )
            if google_user:
                return TokenCreator(google_user.user_id).auth_tokens

            username = generate_auth_code()

            user = await self.user_creator.execute(name, username)

            await self.oauth.create_item(
                user_id=user.id, provider=ProviderType.GOOGLE, provider_id=google_id
            )

            return TokenCreator(user.id).auth_tokens


