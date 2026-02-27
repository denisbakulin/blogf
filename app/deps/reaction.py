from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.reaction import ReactionService


def get_reaction_service(
        session: getSessionDep
) -> ReactionService:
    return ReactionService(session=session)


reactionServiceDep = Annotated[ReactionService, Depends(get_reaction_service)]


