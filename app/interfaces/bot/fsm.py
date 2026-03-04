from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis


redis_client = Redis.from_url("redis://localhost:6379")

storage = RedisStorage(redis=redis_client)


class Waiting(StatesGroup):
    password = State()
