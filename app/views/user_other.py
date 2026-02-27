# from deps.comment import commentServiceDep
# from deps.post import postServiceDep
from fastapi import APIRouter, Depends
from helpers.search import Pagination
# from schemas.post import PostShow
# from schemas.topic import UserCommentsCountOfTopicShow
from schemas.user import UserShow, UserProfileShow
from deps.user import userDep, userServiceDep, userLogicDep
from utils.user import UserSearchParams


user_router = APIRouter(prefix="/users", tags=["👨 Пользователи"])

@user_router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],
)
async def search_users(
        logic: userLogicDep,
        search: UserSearchParams = Depends(),
        pagination: Pagination = Depends(),
):
    return await logic.search(search=search, pagination=pagination)



@user_router.get(
    "/@{username}",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
        user: userDep,
        logic: userLogicDep
):
    return await logic.get_profile(user)



# @user_router.get(
#     "/@{username}/posts",
#     summary="Получить посты пользователя",
#     response_model=list[PostShow],
# )
# async def get_user_posts(
#         user: userDep,
#         service: postServiceDep,
#         pagination: Pagination = Depends()
# ):
#     return await service.get_user_posts(user=user, pagination=pagination)




#
# @user_router.get(
#     "/@{username}/top-topics",
#     summary="Получить топ обсуждений",
#     response_model=list[UserCommentsCountOfTopicShow],
# )
# async def get_top_topics(
#         user: userDep,
#         service: commentServiceDep,
# ):
#     return await service.get_top_themes_of_user(user.id)





