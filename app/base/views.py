from fastapi import APIRouter

root = APIRouter(prefix="", tags=["Главная"])


@root.get("/", summary="Hello)")
def get_root():
    return {"msg": "hello"}


@root.get("/health", summary="Проверка")
def heath():
    return {"ok": True}



