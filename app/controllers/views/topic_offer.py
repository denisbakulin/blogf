from deps.auth import currentUserDep
from deps.topic import topicServiceDep
from deps.topic_offer import topicOfferServiceDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.topic import AddTopicByOffer
from schemas.topic_offer import CreateTopicOffer, TopicOfferFullShow, TopicOfferShow, UserUsername
from base.db import getSessionDep
from logic import CreateTopicFromOfferUseCase

router = APIRouter(prefix="/topic-offers", tags=["📚 Предложенные Темы"])


@router.post(
    "",
    summary="Предложить тему для обсуждений",
    status_code=status.HTTP_201_CREATED,
    response_model=TopicOfferShow
)
async def create_topic_offer(
        topic_create: CreateTopicOffer,
        user: currentUserDep,
        service: topicOfferServiceDep,
):
    offer = await service.create_offer_topic(
        author_id=user.id, topic_create=topic_create
    )

    return TopicOfferShow.from_orm(offer)



@router.get(
    "",
    summary="Посмотреть предложенные темы",
    response_model=list[TopicOfferFullShow]
)
async def get_offer_topics(
        service: topicOfferServiceDep,
        pagination: Pagination = Depends()
):
    offers = await service.get_topic_offers(pagination)

    return [
        TopicOfferFullShow(
            **TopicOfferShow.from_orm(offer).model_dump(),
            author=UserUsername.from_orm(author),
            process_user=UserUsername.from_orm(processor) if processor else None
        ) for offer, author, processor in offers
    ]



@router.get(
    "/{offer_id}",
    summary="Получить тему для обсуждений",
    response_model=TopicOfferFullShow
)
async def get_topic_offer(
        offer_id: int,
        service: topicOfferServiceDep,
):
    offer, author, processor = await service.get_topic_offer_by_id(offer_id)

    return TopicOfferFullShow(
        **TopicOfferShow.from_orm(offer).model_dump(),
        author=UserUsername.from_orm(author),
        process_user=UserUsername.from_orm(processor) if processor else None
    )

#todo доступ админам + добавить таблицу админов


@router.post(
    "/{offer_id}/process",
    summary="Принять/отклонить тему",
    status_code=status.HTTP_201_CREATED
)
async def process_topic(
    session: getSessionDep,
    offer_id: int,
    process: AddTopicByOffer,
    user: currentUserDep
):
    logic = CreateTopicFromOfferUseCase(session)


    return await logic.execute(
        user=user, process=process, offer_id=offer_id
    )
