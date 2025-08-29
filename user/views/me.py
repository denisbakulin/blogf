from fastapi import APIRouter, Depends, HTTPException
from user.schemas import UserShow, UserUpdate, UserShowMe, PasswordChange
from auth.dependencies import get_current_user
from user.models import User
from user.service import UserService
from user.dependencies import get_user_service
from user.exceptions import UserAlreadyExistErr, IncorrectPasswordErr

me_router = APIRouter(prefix="/me", tags=["me"])


@me_router.get("", response_model=UserShow)
async def get_me(
        me: User = Depends(get_current_user)
):
    return me

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
