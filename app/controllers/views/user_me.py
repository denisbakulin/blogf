from base.db import getSessionDep
from deps.auth import currentUserDep
from services.comment import CommentService
from services.reaction import ReactionService
from deps.user import userServiceDep
from entities import ReactionType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.comment import CommentShow, CommentAuthorShow, CommentFullShow
from schemas.post import PostCreate, PostShow, PostSlug
from schemas.reaction import ReactionShow, ReactionAuthorShow, ReactionPostShow
from schemas.user import UserProfile, UserProfileShow, UserSettings, UserShow, UserUpdate
from logic import CreateWallPostUseCase,  UpdateWallUseCase
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




@router.get(
    "/comments",
    summary="Получить комментарии текущего пользователя",
    response_model=list[CommentFullShow]
)
async def get_my_comments(
        user: currentUserDep,
        session: getSessionDep,
        pagination: Pagination = Depends()
):

    service = CommentService(session)

    comments = await service.get_user_comments(
        user_id=user.id, pagination=pagination
    )

    return [
        CommentFullShow(
            **CommentShow.from_orm(comment).model_dump(),
            author_username=user.username,
            post_slug=post.slug,
        )
        for comment, user, post in comments
    ]



@router.get(
    "/reactions",
    summary="Получить реакции пользователя",
    response_model=list[ReactionPostShow]
)
async def get_my_reactions(
        user: currentUserDep,
        session: getSessionDep,
        r: ReactionType | None = None,
        pagination: Pagination = Depends()
):

    service = ReactionService(session)

    reactions = await service.get_user_reactions(
        user_id=user.id, reaction_type=r, pagination=pagination
    )

    return [
        ReactionPostShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            post=PostSlug.from_orm(post)
        )
        for reaction, post in reactions
    ]




@router.post(
    "/posts",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
    response_model=PostShow
)
async def create_post(
        create: PostCreate,
        user: currentUserDep,
        session: getSessionDep
):

    logic = CreateWallPostUseCase(session)
    post = await logic.execute(wall_owner_id=user.id, create=create)

    return PostShow.from_orm(post)

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













