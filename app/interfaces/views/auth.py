from fastapi import APIRouter, Cookie, HTTPException, Response, Request

from deps.auth import (baseAuthServiceDep, currentUserDep,
                       googleAuthServiceDep, tgAuthServiceDep)
from exceptions.auth import InvalidTokenError
from schemas.auth import (AccessTokenResponse, AuthCreds, ForgetPassword,
                          PasswordChange, ResetPassword, LoginGoogle, LoginTelegram)
from utils.auth import (TokenCreator, TokenTypes, get_decoded_token,
                        set_refresh_token_cookie)

auth_router = APIRouter(prefix="/auth", tags=["🔐 Авторизация"])


@auth_router.post(
    "/login",
    summary="Войти в аккаунт по паролю",
    response_model=AccessTokenResponse,
)
async def login_user(
        response: Response,
        creds: AuthCreds,
        service: baseAuthServiceDep,
        request: Request
):
    host = request.client.host

    tokens = await service.login(creds, host)
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

    decoded_token = get_decoded_token(token=refresh_token)

    if decoded_token.type != TokenTypes.refresh:
        raise InvalidTokenError("Тип токена не access")

    access_token = TokenCreator(user_id=decoded_token.user_id).access

    return AccessTokenResponse(access_token=access_token)


@auth_router.put(
    "/password",
    summary="Изменить пароль"
)
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        service: baseAuthServiceDep,
):
    await service.change_password(user=user, pwd=pwd)



@auth_router.post(
    "/forget-password",
    summary="Забыл пароль",
)
async def forget_password(
        forget: ForgetPassword,
        auth_service: baseAuthServiceDep
):
    return await auth_service.forget_password(forget.username)


@auth_router.post(
    "/reset-password",
    summary="Пересоздать пароль",
)
async def reset_password(
        code: str,
        pwd: ResetPassword,
        auth_service: tgAuthServiceDep
):
    return await auth_service.reset_password(
        code=code, password=pwd.password
    )



@auth_router.get(
    "/telegram/verify-account",
    summary="Верифицировать аккаунт через Telegram",
)
async def telegram_verify(
        user: currentUserDep,
        telegram: tgAuthServiceDep
):
    code = await telegram.auth_code.create("verify", user.id)
    return {"url": telegram.get_verify_ref(code)}



@auth_router.post(
    "/telegram/login",
    summary="Вход через Telegram",
    response_model=AccessTokenResponse
)
async def login_with_telegram(
        login: LoginTelegram,
        service: tgAuthServiceDep,
        response: Response
):

    result = await service.login(token=login.token, name=login.name)
    set_refresh_token_cookie(response, result.refresh)
    return AccessTokenResponse(access_token=result.access)


@auth_router.get(
    "/google/ref",
    summary="Ссылка на google страницу"
)
async def google_ref(
        google: googleAuthServiceDep
):
    return {"url": google.oauth_uri}


@auth_router.post(
    "/google/login",
    summary="Логин через google"
)
async def login_google(
        google: googleAuthServiceDep,
        login: LoginGoogle,
        response: Response
):
    tokens = await google.login(login.code)
    set_refresh_token_cookie(response, tokens.refresh)
    return AccessTokenResponse(access_token=tokens.access)



