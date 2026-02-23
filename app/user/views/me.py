from auth.deps import currentUserDep
from comment.deps import commentServiceDep
from comment.schemas import CommentShow
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from post.deps import postServiceDep
from post.schemas import PostAllows, PostCreate, PostShow
from reaction.deps import reactionServiceDep
from reaction.schemas import PostReactionShow, TopicReactionShow
from reaction.types import ReactionsGetParams
from user.deps import userServiceDep
from user.schemas import PasswordChange, UserSettings, UserShowMe, UserUpdate

me_router = APIRouter(prefix="/me", tags=["👤 Личный кабинет"])


@me_router.get(
    "",
    summary="Получить текущего пользователя",
    response_model=UserShowMe,
)
async def get_me(
        user: currentUserDep
):
    return user


@me_router.patch(
    "",
    summary="Изменить информацию текущего пользователя",
    response_model=UserShowMe
)
async def patch_my_info(
        user_update: UserUpdate,
        user: currentUserDep,
        service: userServiceDep,
):
    return await service.update_user(user=user, user_update=user_update)




@me_router.put(
    "/password",
    summary="Изменить пароль"
)
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        service: userServiceDep,
):
    await service.change_password(
        user, pwd.old_password, pwd.new_password
    )

@me_router.get(
    "/settings",
    summary="Получить настройки аккаунта",
    response_model=UserSettings
)
async def get_settings(
        user: currentUserDep,
):

    return user.settings


@me_router.patch(
    "/settings",
    summary="Изменить настройки аккаунта",
    response_model=UserSettings
)
async def edit_settings(
        user: currentUserDep,
        service: userServiceDep,
        settings: UserSettings
):
    return await service.edit_user_settings(user, settings)


@me_router.get(
    "/comments",
    summary="Получить комментарии текущего пользователя",
    response_model=list[CommentShow],

)
async def get_my_comments(
        user: currentUserDep,
        service: commentServiceDep,
        pagination: Pagination = Depends()

):
    return await service.get_user_comments(user=user, pagination=pagination)




@me_router.get(
    "/reactions",
    summary="Получить реакции пользователя",
    response_model=list[PostReactionShow | TopicReactionShow],

)
async def get_my_reactions(
        user: currentUserDep,
        like_service: reactionServiceDep,
        v: ReactionsGetParams,
        pagination: Pagination = Depends()
):
    return await like_service.get_user_reactions(user, v, pagination)




@me_router.post(
    "/posts",
    summary="Создать пост",
    response_model=PostShow,
    status_code=status.HTTP_201_CREATED,

)
async def create_post(
        post_create: PostCreate,
        post_allows: PostAllows,
        user: currentUserDep,
        post_service: postServiceDep,
):
    return await post_service.create_post(user=user, post_create=post_create, allows=post_allows)












