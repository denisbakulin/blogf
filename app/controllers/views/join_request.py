from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter

from logic import (
    GetJRSUseCase,
    ProcessJRSPUseCase,
)
from schemas.channel import ChannelID

from schemas.join_request import JRSUserShow, JRShow
from schemas.user import UserUsername


router = APIRouter(prefix="/join-requests", tags=["Заявки на вступление"])


@router.get(
    "/channels/{channel_id}",
    summary="Получить заявки в канал",
    response_model=list[JRSUserShow]
)
async def get_jrs(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
):
    logic = GetJRSUseCase(session)

    jrs = await logic.execute(user=user, channel_id=channel_id)

    return [
        JRSUserShow(
            **JRShow.from_orm(jr).model_dump(),
            user=UserUsername.from_orm(user)
        ) for jr, user in jrs
    ]


@router.post(
    "/process/{jr_id}",
    summary="Обработать заявку",
)
async def process_jr(
    channel: ChannelID,
    session: getSessionDep,
    user: currentUserDep,
    jr_id: int,
    accept: bool
):

    logic = ProcessJRSPUseCase(session)

    await logic.execute(
        channel_id=channel.id, user=user, jr_id=jr_id, accept=accept
    )