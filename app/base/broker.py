from faststream.redis import RedisBroker
from base.settings import settings

broker: RedisBroker = RedisBroker(
    host=settings.redis.host,
    port=settings.redis.port
)








