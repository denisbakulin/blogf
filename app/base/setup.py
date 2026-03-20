from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]


def create_app():
    app = FastAPI(
        lifespan=lifespan,
        debug=True,
        description="Application between blog, telegram and forum "
    )
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
    from controllers.views import routers

    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from base.db import init_models
    await init_models()



@asynccontextmanager
async def lifespan(
        app: FastAPI,
):

    include_routers(app)
    from base.broker import broker

    await init_db(app)

    await broker.start()

    yield

    await broker.stop()


