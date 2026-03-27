from fastapi import APIRouter
from base.db import getSessionDep
from deps.auth import currentUserDep

from logic import CrossToInviteLinkUseCase
router = APIRouter(prefix="/invite-links", tags=["invite link"])


@router.post(
    "/{link}"
)
async def process_invite_link(
    link: str,
    user: currentUserDep,
    session: getSessionDep
):
    logic = CrossToInviteLinkUseCase(session)

    return await logic.execute(link=link, user=user)
    