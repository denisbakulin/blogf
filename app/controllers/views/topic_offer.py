from deps.auth import currentUserDep
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.topic import AddTopicByOffer
from schemas.topic_offer import CreateTopicOffer, TopicOfferFullShow, TopicOfferShow, UserUsername
from base.db import getSessionDep
from logic import CreateTopicFromOfferUseCase
from services.topic_offer import TopicOfferService


router = APIRouter(prefix="/topic-offers", tags=["📚 Предложенные Темы"])


@router.post(
    "",
    summary="Предложить тему для обсуждений",
    status_code=status.HTTP_201_CREATED,
    response_model=TopicOfferShow
)
async def create_topic_offer(
    create: CreateTopicOffer,
    user: currentUserDep,
    session: getSessionDep
):
    service = TopicOfferService(session)

    offer = await service.create_offer_topic(
        author_id=user.id, topic_create=create
    )

    return TopicOfferShow.from_orm(offer)



@router.get(
    "",
    summary="Посмотреть предложенные темы",
    response_model=list[TopicOfferFullShow]
)
async def get_offer_topics(
    session: getSessionDep,
    pagination: Pagination = Depends()
):
    service = TopicOfferService(session)

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
    session: getSessionDep,
):
    service = TopicOfferService(session)

    offer, author, processor = await service.get_topic_offer_by_id(offer_id)

    return TopicOfferFullShow(
        **TopicOfferShow.from_orm(offer).model_dump(),
        author=UserUsername.from_orm(author),
        process_user=UserUsername.from_orm(processor) if processor else None
    )


@router.post(
    "/process/{offer_id}",
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


