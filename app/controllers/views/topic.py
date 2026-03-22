from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.post import postServiceDep
from deps.subscribe import subscribeServiceDep
from deps.topic import topicDep, topicServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.post import PostAuthorShow, PostCreate, PostShow
from schemas.topic import ContainerMetricsShow, CreateTopic, TopicShow, UserUsername
from usecases.post import CreatePostUseCase
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
    response_model=TopicShow
)
async def get_topic(
        topic: topicDep,
        service: topicServiceDep
):
    topic, author = await service.get_topic(topic.id)

    return TopicShow(
        **ContainerMetricsShow.from_orm(topic).model_dump(),
        author=UserUsername.from_orm(author)
    )



@router.post(
    "/{slug}/subscribe",
    summary="Подписаться на тему",
    status_code=status.HTTP_201_CREATED,
    response_model=None
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
    response_model=PostShow
)
async def create_post(
        topic: topicDep,
        create: PostCreate,
        user: currentUserDep,
        session: getSessionDep
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        user=user, post=create, container_id=topic.id
    )

    return PostShow.from_orm(post)


@router.get(
    "/{slug}/posts",
    summary="Получить посты по теме",
    response_model=list[PostAuthorShow]
)
async def get_topic_posts(
        topic: topicDep,
        service: postServiceDep,
        pagination: Pagination = Depends()
):


    posts = await service.get_posts_with_authors(
        container_id=topic.id, pagination=pagination
    )

    return [
        PostAuthorShow(
            **PostShow.from_orm(post).model_dump(),
            author=UserUsername.from_orm(author)
        ) for post, author in posts
    ]








