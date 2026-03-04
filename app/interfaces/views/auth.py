from deps.auth import authServiceDep, currentUserDep, tgAuthServiceDep
from deps.user import userServiceDep
# from deps.tg_verified import tgvServiceDep
# from deps.user import userServiceDep
from exceptions.auth import InvalidTokenError
from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from schemas.auth import (AccessTokenResponse, AuthCreds, TgLoginAnswer,
                          TgAuthCode, LoginTokens, ForgetPassword, PasswordChange)
from schemas.user import UserCreate
from utils.auth import (TokenCreator, TokenTypes, decode_token,
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
        service: authServiceDep
):

    tokens = await service.login(creds)
    set_refresh_token_cookie(response, tokens.refresh)
    return AccessTokenResponse(access_token=tokens.access)


@auth_router.post(
    "/register",
    summary="Зарегистрироваться",
)
async def register_user(
        response: Response,
        user_create: UserCreate,
        service: authServiceDep,
):
    tokens = await service.register(user_create)
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


@auth_router.get(
    "/get-tg-verify-code",
    summary="Получить код верификации для Telegram",
    response_model=TgAuthCode
)
async def get_telegram_verify_code(
        user: currentUserDep,
        auth_service: authServiceDep
):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="уже верефицирован")

    code = await auth_service.auth_code.create("verify", user.id)
    return TgAuthCode(code=code)


@auth_router.get(
    "/telegram/login",
    summary="Вход / Регистрация через Telegram",
    response_model=TgAuthCode | AccessTokenResponse
)
async def login_with_telegram(
        code: str,
        auth_service: tgAuthServiceDep,
        response: Response
):

    result = await auth_service.login_with_telegram(code)

    if isinstance(result, TgAuthCode):
        return result

    set_refresh_token_cookie(response, result.refresh)
    return AccessTokenResponse(access_token=result.access)


@auth_router.post(
    "/telegram/register",
    summary="Зарегистрироваться через телеграм",
    response_model=TgLoginAnswer
)
async def register_user_with_telegram(
        response: Response,
        user_create: UserCreate,
        service: tgAuthServiceDep,
        code: str
):
    tokens = await service.register(user_create, code)
    set_refresh_token_cookie(response, tokens.refresh)
    return tokens



@auth_router.put(
    "/password",
    summary="Изменить пароль"
)
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        service: userServiceDep,
):
    await service.change_password(user=user, pwd=pwd)

@auth_router.post(
    "/forget-password",
    summary="Забыл пароль",
)
async def forget_password(
        forget: ForgetPassword,
        auth_service: authServiceDep
):
    return await auth_service.forget_password(forget.username)


@auth_router.post(
    "/reset-password",
    summary="Пересоздать пароль",
)
async def reset_password(
        code: str,
        auth_service: authServiceDep
):
    return await auth_service.login_with_telegram(code)
