from t.reaction import ReactionsGetParams

from deps.auth import currentUserDep
# from deps.comment import commentServiceDep
# from deps.post import postServiceDep
# from deps.reaction import reactionServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
# from schemas.comment import CommentShow
from schemas.post import PostCreate, PostShow
from schemas.reaction import PostReactionShow, TopicReactionShow
from schemas.user import PasswordChange, UserSettings, UserUpdate, UserShow, UserProfile, UserProfileShow
from deps.user import userServiceDep, userLogicDep
from logic.user import UserLogic
from DTO.user import UserProfileDTO

me_router = APIRouter(prefix="/me", tags=["👤 Личный кабинет"])
from dataclasses import asdict

@me_router.get(
    "",
    summary="Получить текущего пользователя",
    response_model=UserProfileShow,
) #work
async def get_me(
        user: currentUserDep,
        logic: userLogicDep
):
    return await logic.get_profile(user)


@me_router.patch(
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


@me_router.put(
    "/password",
    summary="Изменить пароль"
) #work
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        service: userServiceDep,
):
    await service.change_password(user=user, pwd=pwd)



@me_router.get(
    "/settings",
    summary="Получить настройки аккаунта",
    response_model=UserSettings
)
async def get_settings(
        user: currentUserDep,
        logic: userLogicDep,
):
    return await logic.get_settings(user)


@me_router.patch(
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


# @me_router.get(
#     "/comments",
#     summary="Получить комментарии текущего пользователя",
#     response_model=list[CommentShow],
#
# )
# async def get_my_comments(
#         user: currentUserDep,
#         service: commentServiceDep,
#         pagination: Pagination = Depends()
#
# ):
#     return await service.get_user_comments(user_id=user.id, pagination=pagination)




# @me_router.get(
#     "/reactions",
#     summary="Получить реакции пользователя",
#     response_model=list[PostReactionShow | TopicReactionShow],
#
# )
# async def get_my_reactions(
#         user: currentUserDep,
#         like_service: reactionServiceDep,
#         v: ReactionsGetParams,
#         pagination: Pagination = Depends()
# ):
#     return await like_service.get_user_reactions(user, v, pagination)



#
# @me_router.post(
#     "/posts",
#     summary="Создать пост",
#     response_model=PostShow,
#     status_code=status.HTTP_201_CREATED,
#
# )
# async def create_post(
#         post_create: PostCreate,
#         user: currentUserDep,
#         post_service: postServiceDep,
# ):
#     return await post_service.create_post(user=user, post_create=post_create)












