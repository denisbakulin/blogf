from setup import create_app
from core.exceptions import EntityNotFoundError

app = create_app()


@app.get("/test-error")
async def test_error():
    raise EntityNotFoundError("User not found in /test-error")