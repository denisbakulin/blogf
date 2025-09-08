from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from user.schemas import EmailUpdate, UserUpdate, UserShowMe, PasswordChange
from auth.dependencies import get_current_user
from user.models import User
from user.service import UserService
from user.dependencies import get_user_service
from user.exceptions import UserAlreadyExistErr, IncorrectPasswordErr
from mail.utils import EmailSender
from auth.utils import TokenCreator

me_router = APIRouter(prefix="/me", tags=["me"])


@me_router.get("")
async def get_me(
        user: User = Depends(get_current_user)
) -> UserShowMe:
    return user

@me_router.patch("")
async def patch_my_info(
        user_updates: UserUpdate,
        me: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.update_user(me, user_updates)
        return {"ok": True}

    except UserAlreadyExistErr as e:
        raise HTTPException(401, detail=str(e))


@me_router.put("/password")
async def change_password(
        pwd: PasswordChange,
        me: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.change_password(me, pwd.old_password, pwd.new_password)
        return {"ok": True}
    except IncorrectPasswordErr as e:
        raise HTTPException(401, detail=str(e))


@me_router.put("/email")
async def change_email(
        email: EmailUpdate,
        bg_task: BackgroundTasks,
        me: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.change_email(me, email.new_email)
        ce_token = TokenCreator(me.id).change_email
        bg_task.add_task(
            EmailSender(email.new_email, "Смена почты").change_email,
            ce_token,
            me.username
        )

    except UserAlreadyExistErr as e:
        raise HTTPException(401, detail=str(e))
