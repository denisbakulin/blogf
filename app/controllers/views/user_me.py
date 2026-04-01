from base.db import getSessionDep
from deps.auth import currentUserDep

from deps.user import userServiceDep

from fastapi import APIRouter

from schemas.user import UserProfile, UserProfileShow, UserSettings, UserShow, UserUpdate
from logic import  UpdateWallUseCase
from schemas.container import ContainerUpdate


router = APIRouter(prefix="/me", tags=["👤 Личный кабинет"])


@router.get(
    "",
    summary="Получить текущего пользователя",
    response_model=UserProfileShow,
)
async def get_my_info(
        user: currentUserDep,
        service: userServiceDep
):
    profile = await service.get_user_profile(user.id)
    user = UserShow.from_orm(user)

    return UserProfileShow(
        **user.model_dump(),
        profile=UserProfile.from_orm(profile)
    )



@router.patch(
    "",
    summary="Изменить информацию текущего пользователя",
    response_model=UserProfileShow
)
async def patch_my_info(
        user: currentUserDep,
        update: UserUpdate,
        service: userServiceDep
):
    user = await service.update_user(user=user, update=update)
    profile = await service.get_user_profile(user.id)

    return UserProfileShow(
        **UserShow.from_orm(user).model_dump(),
        profile=UserProfile.from_orm(profile)
    )


@router.get(
    "/settings",
    summary="Получить настройки аккаунта",
    response_model=UserSettings
)
async def get_settings(
        user: currentUserDep,
        service: userServiceDep,
):
    settings = await service.get_user_settings(user.id)

    return UserSettings.from_orm(settings)



@router.patch(
    "/settings",
    summary="Изменить настройки аккаунта",
    response_model=UserSettings
)
async def edit_settings(
        user: currentUserDep,
        update: UserSettings,
        service: userServiceDep,

):
    settings = await service.update_user_settings(user.id, update=update)

    return UserSettings.from_orm(settings)











@router.patch(
    "/wall",
    summary="update my wall info"
)
async def update_wall(
    update: ContainerUpdate,
    session: getSessionDep,
        user: currentUserDep,

):
    logic = UpdateWallUseCase(session)

    await logic.execute(user=user, update=update)













