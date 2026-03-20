from deps.auth import currentUserDep

from deps.post import postServiceDep
from deps.subscribe import subscribeServiceDep
from deps.topic import topicDep, topicServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.post import PostCreate
from schemas.topic import CreateTopic
from utils.container import ContainerSearchParams
from usecases.post import CreatePostUseCase
from base.db import getSessionDep
from entities.container import ContainerType

router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@router.get(
    "",
    summary="Получить темы",
)
async def get_topics(
        service: topicServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_items_by(pagination=pagination, type=ContainerType.TOPIC)



@router.post(
    "",
    summary="Создать тему",
    status_code=status.HTTP_201_CREATED
)
async def create_topic(
        topic: CreateTopic,
        service: topicServiceDep,
        user: currentUserDep
):
    return await service.create_topic(
        topic=topic, author_id=user.id
    )



@router.get(
    "/search",
    summary="Поиск темы по ключевым параметрам",
)
async def search_topics(
        service: topicServiceDep,
        pagination: Pagination = Pagination(),
        search: ContainerSearchParams = Depends(),
):
    return await service.search_topic(search=search, pagination=pagination)



@router.get(
    "/{slug}",
    summary="Получить тему",
)
async def get_topic(
        topic: topicDep,
        service: topicServiceDep
):
    return topic


@router.get(
    "/{slug}/sub",
    summary="Подписаться на тему",
)
async def subscribe_to_topic(
        topic: topicDep,
        service: subscribeServiceDep,
        user: currentUserDep
):
    return await service.create_subscribe(user_id=user.id, container_id=topic.id)



@router.post(
    "/{slug}/posts",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
        topic: topicDep,
        create: PostCreate,
        user: currentUserDep,
        session: getSessionDep
):
    logic = CreatePostUseCase(session)

    return await logic.execute(
        user=user, post=create, container_id=topic.id
    )


@router.get(
    "/{slug}/posts",
    summary="Получить посты по теме",
)
async def get_topic_posts(
        topic: topicDep,
        service: postServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_items_by(
        container_id=topic.id, pagination=pagination
    )








