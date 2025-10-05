import pytest


@pytest.mark.parametrize(
    "reaction_type",
    ["all", "like", "dislike", "love"]
)
@pytest.mark.asyncio
async def test_get_post_reactions(reaction_type, auth_client):
    response = await auth_client.get(
        "/posts/test-post-1/reactions",
        params={"t": reaction_type, "limit": 10, "offset": 0}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for r in response.json():
        assert (reaction_type == "all" or
                r.get("reaction") == reaction_type)
        assert r.get("post_id") == 1


