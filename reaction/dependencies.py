from reaction.service import ReactionService
from fastapi import Depends
from typing import Annotated
from core.db import getSessionDep


def get_reaction_service(
        session: getSessionDep
) -> ReactionService:
    return ReactionService(session=session)


reactionServiceDep = Annotated[ReactionService, Depends(get_reaction_service)]


