import pytest


@pytest.mark.asyncio
async def test_get_user(auth_client):
    response = await auth_client.get(
        f"/users/@{auth_client.user.username}"
    )

    assert response.status_code == 200
    assert response.json().get("username") == auth_client.user.username



@pytest.mark.asyncio
async def test_register(auth_client):
    response = await auth_client.get("/me")

    assert response.status_code == 200
    assert response.json().get("id") == auth_client.user.id


import pytest


@pytest.mark.asyncio
async def test_search_users(client):
    # Нестрогий поиск по username
    response = await client.get(
        "/users/search",
        params={"q": "user", "strict": False, "field": "username"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 1
    assert all("username" in u for u in data)

    # Строгий поиск по username
    response = await client.get(
        "/users/search",
        params={"q": "user1", "strict": True, "field": "username"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == "user1"






