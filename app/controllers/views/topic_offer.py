from deps.auth import currentUserDep

from deps.topic import topicServiceDep
from deps.topic_offer import topicOfferServiceDep, offerTopicDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination

from schemas.topic import AddTopicByOffer
from schemas.topic_offer import CreateTopicOffer

router = APIRouter(prefix="/topic-offers", tags=["📚 Предложенные Темы"])


@router.post(
    "",
    summary="Предложить тему для обсуждений",
    status_code=status.HTTP_201_CREATED,
)
async def create_topic_offer(
        topic_create: CreateTopicOffer,
        user: currentUserDep,
        service: topicOfferServiceDep,
):
    return await service.create_offer_topic(
        author_id=user.id, topic_create=topic_create
    )


@router.get(
    "",
    summary="Посмотреть предложенные темы",
)
async def offer_theme(
        service: topicOfferServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_topic_offers(pagination)


@router.get(
    "/{offer_id}",
    summary="Получить тему для обсуждений",
)
async def get_topic_offer(
        offer_id: int,
        service: topicOfferServiceDep,
):
    return await service.get_topic_offer_by_id(offer_id)


#todo доступ админам + добавить таблицу админов


@router.post(
    "/{offer_id}/process",
    summary="Принять/отклонить тему",
    status_code=status.HTTP_201_CREATED
)
async def process_topic(
        topic_offer: offerTopicDep,
        service: topicServiceDep,
        process: AddTopicByOffer,
        user: currentUserDep
):

    return await service.create_topic_from_offer(
        process=process, topic_offer=topic_offer, process_user_id=user.id
    )
