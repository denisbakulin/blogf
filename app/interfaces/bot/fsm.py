from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis


redis_client = Redis.from_url("redis://localhost:6379")
storage = RedisStorage(redis=redis_client)


class WaitingFSM(StatesGroup):
    password = State()


class ChangeFSM(StatesGroup):
    name = State()
    username = State()
    bio = State()

