
from fastapi import APIRouter, Depends

from allows.deps import allowServiceDep
from allows.schema import AllowBase, AllowShow
from helpers.search import Pagination

allow_router = APIRouter(prefix="/allows", tags=["💬 Права"])













