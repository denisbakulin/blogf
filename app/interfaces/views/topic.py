# from t.reaction import ReactionsGetParams, ReactionsSetParams
# from typing import Literal

from deps.auth import currentUserDep
# from deps.post import postServiceDep
# from deps.reaction import reactionServiceDep
# from deps.subscribe import subscribeServiceDep
from deps.topic import topicDep, topicServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination, search_param_fabric
from schemas.container import ContainerShow, FullContainerShow
# from schemas.post import PostCreate, PostShow
# from schemas.reaction import TopicReactionShow
from schemas.topic import CreateTopic
from utils.container import ContainerSearchParams



topic_router = APIRouter(prefix="/topics", tags=["📚 Темы"])


@topic_router.get(
    "",
    summary="Получить темы",
    response_model=list[ContainerShow]
)
async def get_topics(
        service: topicServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_full_containers(pagination)



@topic_router.post(
    "",
    summary="Создать тему",
    response_model=ContainerShow,
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



@topic_router.get(
    "/search",
    summary="Поиск темы по ключевым параметрам",
    response_model=list[ContainerShow],
)
async def search_topics(
        service: topicServiceDep,
        pagination: Pagination = Pagination(),
        search: ContainerSearchParams = Depends(),
):
    return await service.search_topic(search=search, pagination=pagination)



@topic_router.get(
    "/{slug}",
    summary="Получить тему",
    response_model=FullContainerShow
)
async def get_topic(
        topic: topicDep,
        service: topicServiceDep
):
    return await service.container_service.get_full_container(topic)

#
# @topic_router.get(
#     "/{slug}/sub",
#     summary="Подписаться на тему",
# )
# async def sub_to_topic(
#         topic: topicDep,
#         service: subscribeServiceDep,
#         user: currentUserDep
# ):
#     return await service.create_subscribe(user=user, container_id=topic.id)
#
#
# @topic_router.post(
#     "/{slug}/reactions",
#     summary="Оставить реакцию под темой",
#     response_model=TopicReactionShow,
#     status_code=status.HTTP_201_CREATED
# )
# async def set_topic_reactions(
#         topic: topicDep,
#         user: currentUserDep,
#         reaction: ReactionsSetParams,
#         service: reactionServiceDep
# ):
#     return await service.process_topic_reaction(
#         user=user, container=topic, reaction=reaction
#     )
#
#
#
# @topic_router.get(
#     "/{slug}/reactions",
#     summary="Получить реакции темы",
#     response_model=list[TopicReactionShow],
# )
# async def get_topic_reactions(
#         topic: topicDep,
#         reaction_type: ReactionsGetParams,
#         service: reactionServiceDep,
#         pagination: Pagination = Depends()
# ):
#     return await service.get_topic_reactions(
#         topic=topic, reaction_type=reaction_type, pagination=pagination
#     )
#
#
#
# @topic_router.post(
#     "/{slug}/posts",
#     summary="Создать пост",
#     response_model=PostShow,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_post(
#         topic: topicDep,
#         post_create: PostCreate,
#         user: currentUserDep,
#         service: postServiceDep,
# ):
#     post_create.container_id = topic.id
#
#     return await service.create_post(
#         user=user, post_create=post_create
#     )
#
#
# @topic_router.get(
#     "/{slug}/posts",
#     summary="Получить посты по теме",
#     response_model=list[PostShow]
# )
# async def get_topic_posts(
#         topic: topicDep,
#         service: postServiceDep,
#         pagination: Pagination = Depends()
# ):
#     return await service.get_items_by(
#         container_id=topic.id, pagination=pagination
#     )
#







