import pytest


@pytest.mark.asyncio
async def test_create_post(auth_client):
    response = await auth_client.post(
        "/posts",
        json={
            "title": "hello",
            "content": "test"
        }
    )
    print(response)

    assert response.status_code == 201
    assert response.json().get("id")
    assert response.json().get("slug")


@pytest.mark.asyncio
async def test_get_user_post(auth_client):
    response = await auth_client.get(
        f"/users/@{auth_client.user.username}/posts?limit=3&offset=0"
    )

    posts = response.json()

    assert response.status_code == 200
    assert isinstance(posts, list)

    for post in posts:
        assert isinstance(post, dict)
        assert post.get("slug")
        assert post.get("author_id") == auth_client.user.id




