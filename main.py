from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager


origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
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

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/ping")
def ping():
    return {"msg": "pong"}


if __name__ == "__main__":
    uvicorn.run(app)

