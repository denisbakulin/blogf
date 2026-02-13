from fastapi import APIRouter, Depends, status

from auth.deps import currentUserDep, role_validate
from helpers.search import Pagination
from topic.offrer.deps import ( topicOfferServiceDep, offerTopicDep)
from topic.release.deps import  topicServiceDep
from topic.release.schemas import (AddTopicByOffer)
from topic.offrer.schemas import TopicOfferShow, CreateTopicOffer
from user.model import User, UserRoleEnum


offer_router = APIRouter(prefix="/topic-offers", tags=["📚 Предложенные Темы"])


@offer_router.post(
    "",
    summary="Предложить тему для обсуждений",
    response_model=TopicOfferShow,
    status_code=status.HTTP_201_CREATED,
)
async def offer_theme(
        topic_create: CreateTopicOffer,
        user: currentUserDep,
        service: topicOfferServiceDep,
):
    return await service.create_offer_topic(
        author=user, topic_create=topic_create
    )


@offer_router.get(
    "",
    summary="Посмотреть предложенные темы",
    response_model=list[TopicOfferShow],
)
async def offer_theme(
        service: topicOfferServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_items_by(pagination)


@offer_router.post(
    "/{offer_id}/process",
    summary="Принять/отклонить тему",
    response_model=TopicOfferShow,
    status_code=status.HTTP_201_CREATED
)
async def process_topic(
        topic_offer: offerTopicDep,
        service: topicServiceDep,
        process: AddTopicByOffer,
        user: User = Depends(role_validate(UserRoleEnum.MODERATOR))
):
    return await service.create_topic_from_offer(
        process=process, topic_offer=topic_offer, process_user=user
    )
