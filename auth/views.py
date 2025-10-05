from fastapi import (APIRouter, BackgroundTasks, Cookie, Depends,
                     HTTPException, Response)

from auth.deps import get_auth_service
from auth.exceptions import InvalidTokenError
from auth.schemas import (AccessTokenResponse, AuthCreds)
from auth.service import AuthService
from auth.utils import (TokenCreator, TokenTypes, decode_token,
                        set_refresh_token_cookie)
from mail.utils import EmailSender
from user.schemas import UserCreate

auth_router = APIRouter(prefix="/auth", tags=["🔐 Авторизация"])


@auth_router.post(
    "/register",
    summary="Зарегистрироваться в системе",
    response_model=AccessTokenResponse

)
async def register_user(
        user_info: UserCreate,
        background_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(get_auth_service),

):
    pending_access_token, verify_token = await auth_service.register(user_info)

    background_tasks.add_task(
        EmailSender(user_info.email, "Подтверждение почты").verify_email,
        token=verify_token,
        username=user_info.username,
    )

    return AccessTokenResponse(access_token=pending_access_token)



@auth_router.post(
    "/login",
    summary="Войти в аккаунт",
    response_model=AccessTokenResponse,

)
async def login_user(
        response: Response,
        creds: AuthCreds,
        auth_service: AuthService = Depends(get_auth_service)
):

    tokens = await auth_service.login(creds)
    set_refresh_token_cookie(response, tokens.refresh_token)
    return AccessTokenResponse(access_token=tokens.access_token)



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
    "/verify-by-email",
    summary="Подтвердить почту через переход по ссылке",
    response_model=AccessTokenResponse,

)
async def verify_by_email(
        token: str,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):

    tokens = await auth_service.verify_user_by_email(token)
    set_refresh_token_cookie(response, tokens.refresh_token)

    return AccessTokenResponse(access_token=tokens.access_token)




@auth_router.get(
    "/change-email",
    summary="Сменить почту через переход по ссылке",
    response_model=AccessTokenResponse,

)
async def change_email_by_token(
        token: str,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):
    tokens = await auth_service.verify_new_user_email(token)
    set_refresh_token_cookie(response, tokens.refresh_token)

    return AccessTokenResponse(access_token=tokens.access_token)

