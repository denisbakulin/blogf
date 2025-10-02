import pytest
from tests.conftest import user_info


@pytest.mark.asyncio
async def test_get_user(client):
    response = await client.get(
        f"/users/@{user_info.username}"
    )

    assert response.status_code == 200
    assert response.json().get("username") == user_info.username



