import pytest
from os import getenv
from dotenv import load_dotenv


load_dotenv(".env.test")

@pytest.fixture(scope="session", autouse=True)
def ensure_test_env():
    mode = getenv("APP_MODE")
    if mode != "TEST":
        pytest.exit(f"Окружение [{mode}] не подходит для тестирования!", returncode=1)


from user.service import UserService
from user.schemas import UserCreate
from auth.utils import TokenCreator

user_info = UserCreate(
    username="user",
    password="12345",
    email="user@example.com"
)

import pytest_asyncio
from core.setup import create_app
from core.settings import FirstAdminSettings

from httpx import ASGITransport, AsyncClient

from core.db import get_engine

pytest_plugins = ['pytest_asyncio']

from core.db import session_factory


@pytest_asyncio.fixture(scope="module", autouse=True)
async def db():
    from core.model import BaseORM

    engine = get_engine()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
    await engine.dispose()



@pytest_asyncio.fixture(scope="module")
async def client(db):

    app = create_app()

    lifespan_context = app.router.lifespan_context

    async with lifespan_context(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as ac:
            yield ac

@pytest_asyncio.fixture(scope="module", autouse=True)
async def admin_client(client):
    admin_info = FirstAdminSettings()

    response = await client.post(
        "/auth/login",
        json={
            "username": admin_info.username,
            "password": admin_info.password
        }
    )

    access_token = response.json().get("access_token")

    client.headers.update({"Authorization": f"Bearer {access_token}"})

    return client



@pytest_asyncio.fixture(scope="module", autouse=True)
async def auth_client(client):

    async with session_factory() as session:

        user_service = UserService(session)
        user = await user_service.create_user(user_info, is_verified=True)
        access_token = TokenCreator(user.id).access
        print(user, 1111111111111111)

    if access_token:
        client.headers.update({"Authorization": f"Bearer {access_token}"})

    return client


