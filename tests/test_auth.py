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










