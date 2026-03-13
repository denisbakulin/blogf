from .auth import router as auth_router
from .post import router as post_router
from .topic import router as topic_router
from .comment import comm_router as comm_router
from .user_me import router as me_router
from .user_other import router as user_router
from .subscribe import router as subs_router
from .topic_offer import router as topic_offer_router
from .channel import router as channel_router


routers = [
    auth_router, post_router, topic_router, comm_router,
    me_router, user_router, subs_router, topic_offer_router,
    channel_router
]