from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]


def create_app():
    app = FastAPI(lifespan=lifespan, debug=True)
    set_middlewares(app)
    return app


def set_middlewares(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from base.log import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)

    from base.exceptions_middleware import AppExceptionMiddleware
    app.add_middleware(AppExceptionMiddleware)




def include_routers(app: FastAPI):
    # from allows.view import allow_router
    # from base.views import root
    # from integrations.crypto.views import crypto_router
    # from integrations.weather.views import weather_router
    from views.auth import auth_router
    # from views.channel import channel_router
    from views.comment import comm_router
    # from views.post import post_router
    # from views.subscribe import subs_router
    from views.topic import topic_router
    from views.topic_offer import offer_router
    from views.user_me import me_router
    from views.user_other import user_router

    routers: list[APIRouter] = [
        auth_router, user_router,
         me_router, offer_router,
        comm_router,
        topic_router,
        # post_router, channel_router,
        # crypto_router, weather_router,
        #  subs_router,
       # root, allow_router
    ]


    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from base.db import init_models, session_factory

    await init_models()






@asynccontextmanager
async def lifespan(
        app: FastAPI,
):
    include_routers(app)

    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend
    from redis import asyncio as aioredis

    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await init_db(app)

    yield


