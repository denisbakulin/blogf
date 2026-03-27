from .auth import router as auth_router
from .channel import router as channel_router
from .comment import comm_router as comm_router
from .post import router as post_router
from .subscribe import router as subs_router
from .topic import router as topic_router
from .topic_offer import router as topic_offer_router
from .user_me import router as me_router
from .user_other import router as user_router
from .link import router as il_router
from .admin import router as cadmin_router

routers = [
    auth_router,
    me_router,
    channel_router,
    cadmin_router,
    il_router,
    subs_router,
    user_router,
    post_router,
    comm_router,
    topic_router,
    topic_offer_router,
]