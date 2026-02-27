from base.settings import tg_bot_settings
from deps.auth import authServiceDep, currentUserDep
from deps.tg_verified import tgvServiceDep
from deps.user import userServiceDep
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



@auth_router.post(
    "/bot-verify",
    summary="Ручка для TG бота"
)
async def bot_verify(
        request: Request,
        code: BotVerifyCode,
        user_service: userServiceDep,
        auth_service: authServiceDep,
        tgv_service: tgvServiceDep

):
    secret = request.headers.get("X-Bot-Secret")

    if secret != tg_bot_settings.secret:
        raise HTTPException(status_code=401)

    user_id = await auth_service.check_verify_code(code.code)

    tg_id = await tgv_service.repository.get_one_by(tg_id=code.tg_id)

    if tg_id:
        return {"status": False, "msg": "Вы уже верифицировали аккаунт через Telegram"}
    await tgv_service.create_item(tg_id=code.tg_id)

    if not user_id:
        return {"status": False, "msg": "Код устарел или недействителен, попробуйте еще раз!"}

    if isinstance(user_id, bytes):
        user_id = user_id.decode("utf-8")

    user = await user_service.get_user_by_id(int(user_id))

    await user_service.update_item(user, is_verified=True)
    await auth_service.cache_backand.set(code.code, 0, expire=1)

    return {"status": True, "msg": "Аккаунт успешно верифицирован!"}
