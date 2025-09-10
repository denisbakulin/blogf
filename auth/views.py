from fastapi import Depends, APIRouter, HTTPException, Response, Cookie, BackgroundTasks
from auth.dependencies import get_auth_service
from auth.service import AuthService
from user.schemas import UserCreate
from mail.utils import EmailSender
from user.exceptions import UserAlreadyExistErr, UserNotFoundErr, UserInactiveErr
from auth.utils import set_refresh_token_cookie, decode_token, TokenCreator, TokenTypes
from auth.schemas import AuthCreds
from auth.exceptions import InvalidPasswordErr, InvalidTokenErr


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register_user(
        user_info: UserCreate,
        background_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(get_auth_service),

):
    try:
        pending_access_token, verify_token = await auth_service.register(user_info)
        background_tasks.add_task(
            EmailSender(user_info.email, "Подтверждение почты").verify_email,
            token=verify_token,
            username=user_info.username,
        )
        return {"pending_access_token": pending_access_token}
    except UserAlreadyExistErr as e:
        raise HTTPException(401, str(e))


@auth_router.post("/login")
async def login_user(
        response: Response,
        creds: AuthCreds,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.login(creds)
        set_refresh_token_cookie(response, tokens.refresh_token)
        return {"access_token": tokens.access_token}
    except UserNotFoundErr as e:
        raise HTTPException(404, detail=str(e))
    except (InvalidPasswordErr, UserInactiveErr) as e:
        raise HTTPException(401, detail=str(e))


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token", path="/refresh", secure=True)
    return {"ok": True}


@auth_router.post("/refresh")
async def refresh_token(token: str = Cookie(None)):
    if not token:
        raise HTTPException(401, "No refresh token")
    try:
        decoded_token = decode_token(token=token)

        if decoded_token.type != TokenTypes.refresh:
            raise InvalidTokenErr

        access_token = TokenCreator(user_id=decoded_token.user_id).access

        return {"access_token": access_token}

    except InvalidTokenErr as e:
        raise HTTPException(401, detail=str(e))


@auth_router.get("/verify-by-email")
async def verify_by_email(
        token: str,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.verify_user_by_email(token)
        set_refresh_token_cookie(response, tokens.refresh_token)
        return {"access_token": tokens.access_token}

    except InvalidTokenErr as e:
        raise HTTPException(401, detail=str(e))


@auth_router.get("/change-email")
async def change_email_by_token(
        token: str,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.verify_new_user_email(token)
        set_refresh_token_cookie(response, tokens.refresh_token)
        return {"access_token": tokens.access_token}

    except InvalidTokenErr as e:
        raise HTTPException(401, detail=str(e))