import pytest


@pytest.mark.asyncio
async def test_login(client):

    response = await client.post(
        "/auth/login",
        json={
            "username": "test_admin",
            "password": "test_admin",
        }
    )
    assert response.status_code == 200
    assert response.json().get("access_token")


from tests.conftest import user_info

@pytest.mark.asyncio
async def test_register(auth_client):
    response = await auth_client.get("/me")

    assert response.json().get("username") == user_info.username









