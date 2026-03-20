from deps.comment import commentServiceDep
from deps.reaction import reactionServiceDep
from deps.auth import currentUserDep
from deps.user import userLogicDep
from fastapi import APIRouter, status, Depends
from schemas.post import PostCreate
from usecases.post import CreateWallPostUseCase
from base.db import getSessionDep
from schemas.user import UserProfileShow, UserSettings, UserUpdate
from entities.reaction import ReactionType

router = APIRouter(prefix="/me", tags=["👤 Личный кабинет"])


@router.get(
    "",
    summary="Получить текущего пользователя",
    response_model=UserProfileShow,
) #work
async def get_me(
        user: currentUserDep,
        logic: userLogicDep
):
    return await logic.get_profile(user)


@router.patch(
    "",
    summary="Изменить информацию текущего пользователя",
    response_model=UserProfileShow
) #work
async def patch_my_info(
        user: currentUserDep,
        update: UserUpdate,
        logic: userLogicDep,
):
    return await logic.update(user=user, update=update)




@router.get(
    "/settings",
    summary="Получить настройки аккаунта",
    response_model=UserSettings
)
async def get_settings(
        user: currentUserDep,
        logic: userLogicDep,
):
    return await logic.get_settings(user)


@router.patch(
    "/settings",
    summary="Изменить настройки аккаунта",
    response_model=UserSettings
)
async def edit_settings(
        user: currentUserDep,
        update: UserSettings,
        logic: userLogicDep,

):
    return await logic.update_settings(user=user, update=update)


from helpers.search import Pagination

@router.get(
    "/comments",
    summary="Получить комментарии текущего пользователя",
)
async def get_my_comments(
        user: currentUserDep,
        service: commentServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_user_comments(user_id=user.id, pagination=pagination)



@router.get(
    "/reactions",
    summary="Получить реакции пользователя",

)
async def get_my_reactions(
        user: currentUserDep,
        service: reactionServiceDep,
        r: ReactionType | None = None,
        pagination: Pagination = Depends()
):
    return await service.get_user_reactions(
        user_id=user.id, reaction_type=r, pagination=pagination
    )




@router.post(
    "/posts",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
        create: PostCreate,
        user: currentUserDep,
        session: getSessionDep
):

    logic = CreateWallPostUseCase(session)
    return await logic.execute(wall_owner_id=user.id, create=create)

@router.patch(
    "/wall",
    summary="update my wall info"
)
async def update_wall(

):
    ...












