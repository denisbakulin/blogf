from core.repository import BaseRepository
from reaction.model import Reaction
from sqlalchemy.ext.asyncio import AsyncSession

class ReactionRepository(BaseRepository[Reaction]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session)

