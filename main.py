from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager



origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]


@asynccontextmanager
async def lifespan(
        app: FastAPI,
):

    from user.views.other import user_router
    from user.views.me import me_router
    from auth.views import auth_router
    from post.views import post_router


    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(me_router)
    app.include_router(post_router)



    from core.db import init_models
    from user.models import User, Profile
    from comment.models import Comment
    from post.models import Post


    await init_models()

    from core.config import FirstAdminSettings

    s = FirstAdminSettings.get()

    from admin.views import Admin, UserAdminView, PostAdminView

    admin = Admin(UserAdminView(), PostAdminView())

    app.include_router(admin)


    from core.db import session_factory
    from user.service import UserService

    session = session_factory()

    user_service = UserService(session=session)

    await user_service.create_admin(
        username=s.login,
        password=s.password,
        email=s.email
    )




    yield


app = FastAPI(lifespan=lifespan, debug=True)


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
from core.exceptions import init_error_handlers
init_error_handlers(app)

from core.log import LoggingMiddleware

app.add_middleware(LoggingMiddleware)
@app.get("/ping")
def ping():
    return {"msg": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload_dirs=["."],  # Следить за изменениями в текущей директории
        reload_excludes=["*.tmp", "*.log"],  # Исключить файлы
        log_level="debug"  # Детальное логирование
    )

