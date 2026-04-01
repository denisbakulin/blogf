from starlette import status

from deps.auth import currentUserDep, get_current_user
from base.db import getSessionDep
from deps.container import containerServiceDep
from entities import ContainerType
from logic import GetChannelSubscribersUseCase
from schemas.user import UserShow
from services.channel import PublicChannelService
from services.subscribe import SubscribeService
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.post import PostContainerShow, PostShow
from schemas.container import ContainerShow, ContainerMetricsShow

router = APIRouter(prefix="/subscribes", tags=["🔔 Подписки"])


@router.get(
    "",
    summary="Получить подписки пользователя",
    response_model=list[ContainerMetricsShow]
)
async def get_subs(
    user: currentUserDep,
    session: getSessionDep,
    pagination: Pagination = Depends(),
):
    service = SubscribeService(session)

    subs = await service.get_subs(user_id=user.id, pagination=pagination)

    return [
        ContainerMetricsShow.from_orm(subs)
    ]



@router.get(
    "/content",
    summary="Получить контент подписок",
    response_model=list[PostContainerShow]
)
async def get_subs_content(
    user: currentUserDep,
    session: getSessionDep,
    pagination: Pagination = Depends(),
):
    service = SubscribeService(session)

    content = await service.get_content(
        user_id=user.id, pagination=pagination
    )

    return [
        PostContainerShow(
            **PostShow.from_orm(post).model_dump(),
            container=ContainerShow.from_orm(container)
        ) for post, container in content
    ]



@router.post(
    "/users/{user_id}",
    summary="Подписаться на пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
async def subscribe_to_user_wall(
    user_id: int,
    cuser: currentUserDep,
    session: getSessionDep,
    c: containerServiceDep
):
    service = SubscribeService(session)
    container = await c.get_by_or_raise(author_id=user_id, type=ContainerType.WALL)
    return await service.create_subscribe(user_id=cuser.id, container_id=container.id)



@router.post(
    "/channels/{channel_id}",
    summary="Подписаться на публичный канал",
    status_code=status.HTTP_201_CREATED
)
async def subscribe_to_public_channel(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
):
    channel_service = PublicChannelService(session)
    subscribe_service = SubscribeService(session)

    channel = await channel_service.get_channel(channel_id)

    return await subscribe_service.create_subscribe(
        user_id=user.id, container_id=channel.id
    )



@router.get(
    "/channels/{channel_id}",
    summary="Получить подписчиков канала",
    response_model=list[UserShow]
)
async def get_channel_subscribers(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends()
):
    logic = GetChannelSubscribersUseCase(session)

    users = await logic.execute(
        user=user, channel_id=channel_id, pagination=pagination
    )

    return [
        UserShow.from_orm(user) for user in users
    ]



@router.post(
    "/topics/{topic_id}",
    summary="Подписаться на тему",
    status_code=status.HTTP_201_CREATED,
)
async def subscribe_to_topic(
    topic_id: int,
    session: getSessionDep,
    user: currentUserDep
):
    service = SubscribeService(session)

    return await service.create_subscribe(user_id=user.id, container_id=topic_id)


@router.get(
    "/topics/{topic_id}",
    summary="Получить подписчиков темы",
    dependencies=[Depends(get_current_user)],
    response_model=list[UserShow],
)
async def get_topic_subscribers(
    topic_id: int,
    session: getSessionDep,
    pagination: Pagination = Depends()
):
    service = SubscribeService(session)

    subscribers = await service.get_container_subscribers(
        pagination=pagination, container_id=topic_id,
    )

    return [
        UserShow.from_orm(user) for user in subscribers
    ]
