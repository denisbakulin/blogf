from fastapi import APIRouter, BackgroundTasks, Depends

from auth.dependencies import currentUserDep
from auth.utils import TokenCreator
from comment.dependencies import commentServiceDep
from comment.schemas import CommentShow
from helpers.search import Pagination
from mail.utils import EmailSender
from reaction.dependencies import reactionServiceDep
from reaction.schemas import ReactionShow
from reaction.types import UserReactions
from user.dependencies import userServiceDep
from user.schemas import EmailUpdate, PasswordChange, UserShowMe, UserUpdate

me_router = APIRouter(prefix="/me", tags=["me"])


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
    summary="Изменить информацию текущего пользователя"
)
async def patch_my_info(
        user_updates: UserUpdate,
        user: currentUserDep,
        user_service: userServiceDep,
):
    await user_service.update_user(user, user_updates)



@me_router.put(
    "/password",
    summary="Изменить пароль"
)
async def change_password(
        pwd: PasswordChange,
        user: currentUserDep,
        user_service: userServiceDep,
):

    await user_service.change_password(user, pwd.old_password, pwd.new_password)




@me_router.put(
    "/email",
    summary="Изменить почту"
)
async def change_email(
        email: EmailUpdate,
        bg_task: BackgroundTasks,
        user: currentUserDep,
        user_service: userServiceDep,
):

    await user_service.change_email(user, email.new_email)
    ce_token = TokenCreator(user.id).change_email
    bg_task.add_task(
        EmailSender(email.new_email, "Смена почты").change_email,
        ce_token,
        user.username
    )


@me_router.get(
    "/comments",
    summary="Получить комментарии текущего пользователя",
    response_model=list[CommentShow],

)
async def get_my_comments(
        user: currentUserDep,
        comment_service: commentServiceDep,
        pagination: Pagination = Depends()

):
    return await comment_service.get_user_comments(user=user, pagination=pagination)


@me_router.get(
    "/reactions",
    summary="Получить реакции пользователя",
    response_model=list[ReactionShow],

)
async def get_my_reactions(
        user: currentUserDep,
        like_service: reactionServiceDep,
        v: UserReactions,
        pagination: Pagination = Depends()
):
    return await like_service.get_user_reactions(user, v, pagination)





