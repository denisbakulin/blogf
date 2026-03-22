from redis.asyncio import Redis
from base.settings import settings

cache = Redis(
    decode_responses=True,
    host=settings.redis.host,
    port=settings.redis.port
)

def init_fastapi_cache():
    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend

    FastAPICache.init(RedisBackend(cache), prefix="fastapi-cache")


