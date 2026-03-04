from redis.asyncio import Redis


cache = Redis(
    decode_responses=True
)

def init_fastapi_cache():
    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend

    FastAPICache.init(RedisBackend(cache), prefix="fastapi-cache")


