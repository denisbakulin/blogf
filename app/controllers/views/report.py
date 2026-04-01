from base.db import getSessionDep
from base.model import DBEntity
from deps.auth import currentUserDep

from fastapi import APIRouter
from logic import  GetPostUseCase, GetCommentUseCase
from schemas.report import CreateReport
from services.report import ReportService
from services.topic_offer import TopicOfferService
from services.user import UserService

router = APIRouter(prefix="/report", tags=["Репорт"])



@router.post(
    "/posts/{post_id}",
    summary="зарепортить пост"
)
async def report_post(
    session: getSessionDep,
    post_id: int,
    user: currentUserDep,
    create: CreateReport
):
    logic = GetPostUseCase(session)
    report = ReportService(session)

    post, _ = await logic.execute(
        post_id=post_id,  user=user
    )

    await report.create_item(
        author_id=user.id,
        entity_id=post.id,
        entity_type=DBEntity.POST,
        reason=create.reason
    )




@router.post(
    "/comments/{comment_id}",
    summary="зарепортить комментарий",
)
async def report_comment(
    comment_id: int,
    user: currentUserDep,
    session: getSessionDep,
    create: CreateReport
):
    logic = GetCommentUseCase(session)
    comment = await logic.execute(
        comment_id=comment_id, user=user
    )
    report = ReportService(session)

    await report.create_item(
        author_id=user.id,
        entity_id=comment.id,
        entity_type=DBEntity.COMMENT,
        reason=create.reason
    )


@router.post(
    "/users/{user_id}",
    summary="зарепортить пользователя",
)
async def report_user(
    user_id: int,
    session: getSessionDep,
    user: currentUserDep,
    create: CreateReport
):
    user_service = UserService(session)
    await user_service.get_user_by_id(user_id)

    report = ReportService(session)

    await report.create_item(
        author_id=user.id,
        entity_id=user.id,
        entity_type=DBEntity.USER,
        reason=create.reason
    )



@router.post(
    "/topic-offers/{offer_id}",
    summary="зарепортить offer",
)
async def report_offer(
    offer_id: int,
    user: currentUserDep,
    session: getSessionDep,
    create: CreateReport,
):
    service = TopicOfferService(session)
    report = ReportService(session)

    offer = await service.get_item_by_id(offer_id)

    await report.create_item(
        author_id=user.id,
        entity_id=offer.id,
        entity_type=DBEntity.TOPIC_OFFER,
        reason=create.reason
    )

