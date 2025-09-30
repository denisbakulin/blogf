from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager


origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
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

    from core.log import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)

    from core.exceptions_middleware import AppExceptionMiddleware

    app.add_middleware(AppExceptionMiddleware)



def include_routers(app: FastAPI):
    from user.views.other import user_router
    from user.views.me import me_router
    from auth.views import auth_router
    from post.views import post_router
    from comment.views import comm_router
    from admin.views import Admin, UserAdminView, PostAdminView

    admin_router = Admin(UserAdminView(), PostAdminView())

    routers: list[APIRouter] = [
        user_router,
        me_router,
        auth_router,
        post_router,
        comm_router,
        admin_router
    ]

    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from user.model import User, Profile
    from comment.model import Comment
    from post.model import Post
    from reaction.model import Reaction

    from core.db import session_factory, init_models
    from user.service import UserService
    from user.schemas import UserCreate

    await init_models()

    from core.config import FirstAdminSettings

    admin_data = FirstAdminSettings.get().dict()

    async with session_factory() as session:
        user_service = UserService(session=session)

        await user_service.create_first_admin(
            UserCreate(**admin_data)
        )


@asynccontextmanager
async def lifespan(
        app: FastAPI,
):
    include_routers(app)

    await init_db(app)

    yield


