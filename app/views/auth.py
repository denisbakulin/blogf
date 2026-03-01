from deps.auth import authServiceDep, currentUserDep
# from deps.tg_verified import tgvServiceDep
# from deps.user import userServiceDep
from exceptions.auth import InvalidTokenError
from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from schemas.auth import (AccessTokenResponse, AuthCreds, BotVerifyCode,
                          VerifyCode)
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
    summary="Зарегистрироваться"
)
async def register_user(
        response: Response,
        user_create: UserCreate,
        service: authServiceDep
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
    "/get-verify-code",
    summary="Получить код верификации",
    response_model=VerifyCode
)
async def get_verify_code(
        user: currentUserDep,
        auth_service: authServiceDep
):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="уже верефицирован")

    code = await auth_service.create_verify_code(user_id=user.id)
    return VerifyCode(code=code)




