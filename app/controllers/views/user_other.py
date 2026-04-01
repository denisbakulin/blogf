from base.db import getSessionDep
from deps.auth import currentUserDep
from services.comment import CommentService
from deps.container import containerServiceDep
from services.subscribe import SubscribeService
from deps.user import userServiceDep
from entities import ContainerType, Report
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.container import ContainerMetricsShow
from schemas.post import PostShow
from schemas.user import UserProfile, UserProfileShow, UserShow
from logic import GetWallPostsUseCase
from utils.user import UserSearchParams
from schemas.topic import UserCommentsCountOfTopicShow
from services.report import ReportService
from services.user import UserService
from base.model import DBEntity
from schemas.report import CreateReport

router = APIRouter(prefix="/users", tags=["👨 Пользователи"])

@router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],
)
async def search_users(
    service: userServiceDep,
    search: UserSearchParams = Depends(),
    pagination: Pagination = Depends(),
):
    users = await service.search_users(search=search, pagination=pagination)

    return [
        UserShow.from_orm(user)
        for user in users
    ]


@router.get(
    "/{user_id}",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
    user_id: int,
    service: userServiceDep
):
    user = await service.get_user_by_id(user_id)
    profile = await service.get_user_profile(user_id)

    return UserProfileShow(
        **UserShow.from_orm(user).model_dump(),
        profile=UserProfile.from_orm(profile)
    )





@router.get(
    "/{user_id}/top-topics",
    summary="Получить топ обсуждений пользователя по кол-ву комментариев",
    response_model=list[UserCommentsCountOfTopicShow]
)
async def get_top_topics(
    user_id: int,
    session: getSessionDep,
):
    service = CommentService(session)

    top = await service.get_top_themes_of_user(user_id)

    return [
        UserCommentsCountOfTopicShow(topic_slug=topic.slug, count=count)
        for topic, count in top
    ]



@router.get(
    "/{user_id}/wall",
    summary="Получить стену пользователя",
    response_model=ContainerMetricsShow
)
async def get_user_wall(
    user_id: int,
    service: containerServiceDep,
):
    wall = await service.get_by_or_raise(
        author_id=user_id, type=ContainerType.WALL
    )

    return ContainerMetricsShow.from_orm(wall)












