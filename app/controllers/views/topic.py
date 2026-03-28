from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.post import postServiceDep
from services.subscribe import SubscribeService
from deps.topic import topicServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.post import PostAuthorShow, PostCreate, PostShow
from schemas.topic import ContainerMetricsShow, CreateTopic, TopicShow, UserUsername
from logic import CreatePostUseCase, CreateTopicUseCase
from utils.container import ContainerSearchParams

router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@router.get(
    "",
    summary="Получить темы",
    response_model=list[TopicShow]
)
async def get_topics(
        service: topicServiceDep,
        pagination: Pagination = Depends()
):
    topics = await service.get_topics(pagination=pagination)

    return [
        TopicShow(
            **ContainerMetricsShow.from_orm(topic).model_dump(),
            author=UserUsername.from_orm(author)
        ) for topic, author in topics
    ]



@router.post(
    "",
    summary="Создать тему",
    status_code=status.HTTP_201_CREATED,
)
async def create_topic(
    create: CreateTopic,
    session: getSessionDep,
    user: currentUserDep
):
    logic = CreateTopicUseCase(session)

    return await logic.execute(user=user, create=create)





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
    "/{topic_id}",
    summary="Получить тему",
    response_model=TopicShow
)
async def get_topic(
        topic_id: int,
        service: topicServiceDep
):
    topic, author = await service.get_full_topic(topic_id)

    return TopicShow(
        **ContainerMetricsShow.from_orm(topic).model_dump(),
        author=UserUsername.from_orm(author)
    )



@router.post(
    "/{topic_id}/subscribe",
    summary="Подписаться на тему",
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
async def subscribe_to_topic(
    topic_id: int,
    session: getSessionDep,
    user: currentUserDep
):
    service = SubscribeService(session)

    return await service.create_subscribe(user_id=user.id, container_id=topic_id)



@router.post(
    "/{topic_id}/posts",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
    response_model=PostShow
)
async def create_post(
        topic_id: int,
        create: PostCreate,
        user: currentUserDep,
        session: getSessionDep
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        user=user, post=create, container_id=topic_id
    )

    return PostShow.from_orm(post)


@router.get(
    "/{topic_id}/posts",
    summary="Получить посты по теме",
    response_model=list[PostAuthorShow]
)
async def get_topic_posts(
        topic_id: int,
        service: postServiceDep,
        pagination: Pagination = Depends()
):

    posts = await service.get_posts_with_authors(
        container_id=topic_id, pagination=pagination
    )

    return [
        PostAuthorShow(
            **PostShow.from_orm(post).model_dump(),
            author=UserUsername.from_orm(author)
        ) for post, author in posts
    ]








