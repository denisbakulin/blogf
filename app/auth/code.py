from typing import Literal, TypeAlias

from redis.asyncio import Redis

from utils.auth import generate_auth_code

codeType: TypeAlias = Literal["used_login", "verify", "forget_password"]



class AuthCodeManager:
    def __init__(self, redis: Redis, prefix: str = "tg", ttl: int = 600):
        self.cache = redis
        self.prefix = prefix
        self.ttl = ttl


    async def create(self, type_: codeType, id_: str, code: str =None) -> str:
        code = code or generate_auth_code()
        await self.cache.set(
            f"{self.prefix}:code:{type_}:{code}", id_, ex=self.ttl
        )
        return code

    async def get_id(self, type_: codeType, code: str) -> str | None:
        return await self.cache.get(f"{self.prefix}:code:{type_}:{code}")



    async def delete(self, type_: codeType, code: str) -> None:
        await self.cache.delete(f"{self.prefix}:code:{type_}:{code}")
