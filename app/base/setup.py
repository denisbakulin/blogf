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
    from admin.views import admin_router
    from auth.views import auth_router
    from base.views import root
    from comment.views import comm_router

    from integrations.crypto.views import crypto_router
    from integrations.weather.views import weather_router
    from post.views import post_router
    from sub.views import subs_router
    from topic.release.view import topic_router
    from topic.offrer.view import offer_router
    from user.views.me import me_router
    from user.views.other import user_router
    from channel.view import channel_router
    from allows.view import allow_router

    routers: list[APIRouter] = [
        auth_router, user_router,
        me_router, topic_router, channel_router, offer_router,
        post_router, comm_router,
        crypto_router, weather_router,
         subs_router,
        admin_router, root, allow_router
    ]


    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from base.db import init_models, session_factory

    await init_models()



    async with session_factory() as session:
        from user.service import UserService
        from base.settings import anon_settings, super_admin_settings
        from user.schemas import UserCreate

        user_service = UserService(session=session)

        await user_service.create_super_admin(
            UserCreate(**super_admin_settings.model_dump())
        )

        await user_service.create_anon(
            UserCreate(**anon_settings.model_dump())
        )








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


