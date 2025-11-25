from fastapi import APIRouter, Cookie, Depends, HTTPException, Response

from auth.deps import get_auth_service
from auth.exceptions import InvalidTokenError
from auth.schemas import AccessTokenResponse, AuthCreds
from auth.service import AuthService
from auth.utils import (TokenCreator, TokenTypes, decode_token,
                        set_refresh_token_cookie)
from user.schemas import UserCreate

auth_router = APIRouter(prefix="/auth", tags=["🔐 Авторизация"])

@auth_router.post(
    "/login",
    summary="Войти в аккаунт по паролю",
    response_model=AccessTokenResponse,
)
async def login_user(
        response: Response,
        creds: AuthCreds,
        auth_service: AuthService = Depends(get_auth_service)
):

    tokens = await auth_service.login(creds)
    set_refresh_token_cookie(response, tokens.refresh)
    return AccessTokenResponse(access_token=tokens.access)

@auth_router.post(
    "/register",
    summary="Зарегистрироваться"
)
async def register_user(
        response: Response,
        user_create: UserCreate,
        auth_service: AuthService = Depends(get_auth_service)
):
    tokens = await auth_service.register(user_create)
    set_refresh_token_cookie(response, tokens.refresh)
    return AccessTokenResponse(access_token=tokens.access)


@auth_router.post(
    "/logout",
    summary="Выйти из аккаунта"
)
async def logout(response: Response):
    response.delete_cookie("refresh_token", path="/", secure=True)



@auth_router.post(
    "/refresh",
    summary="Обновить токен доступа"
)
async def refresh_user_token(refresh_token: str = Cookie(None)):

    if not refresh_token:
        raise HTTPException(401, "No refresh token")

    decoded_token = decode_token(token=refresh_token)

    if decoded_token.type != TokenTypes.refresh:
        raise InvalidTokenError("Тип токена не access")

    access_token = TokenCreator(user_id=decoded_token.user_id).access

    return AccessTokenResponse(access_token=access_token)



