from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from user.schemas import EmailUpdate, UserUpdate, UserShowMe, PasswordChange
from auth.dependencies import currentUserDep
from user.models import User
from user.dependencies import userServiceDep
from user.exceptions import UserAlreadyExistErr, IncorrectPasswordErr
from mail.utils import EmailSender
from auth.utils import TokenCreator

me_router = APIRouter(prefix="/me", tags=["me"])


@me_router.get(
    "",
    response_model=UserShowMe
)
async def get_me(
        user: currentUserDep
):
    return user

@me_router.patch("")
async def patch_my_info(
        user_updates: UserUpdate,
        user: currentUserDep,
        user_service: userServiceDep,
):
    try:
        await user_service.update_user(user, user_updates)
        return {"ok": True}

    except UserAlreadyExistErr as e:
        raise HTTPException(401, detail=str(e))


@me_router.put("/password")
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        user_service: userServiceDep,
):
    try:
        await user_service.change_password(user, pwd.old_password, pwd.new_password)
        return {"ok": True}
    except IncorrectPasswordErr as e:
        raise HTTPException(401, detail=str(e))


@me_router.put("/email")
async def change_email(
        email: EmailUpdate,
        bg_task: BackgroundTasks,
        user: currentUserDep,
        user_service: userServiceDep,
):
    try:
        await user_service.change_email(user, email.new_email)
        ce_token = TokenCreator(user.id).change_email
        bg_task.add_task(
            EmailSender(email.new_email, "Смена почты").change_email,
            ce_token,
            user.username
        )

    except UserAlreadyExistErr as e:
        raise HTTPException(401, detail=str(e))
