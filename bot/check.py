import aiohttp

from app.base.settings import tg_bot_settings


async def check_verify_code(code: str, tg_id: int) -> dict[str, str]:
    headers = {
        "X-Bot-Secret": tg_bot_settings.secret
    }

    json = {
        "code": code,
        "tg_id": tg_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                "http://localhost:8001/auth/bot-verify",
                json=json,
                headers=headers
        ) as resp:
            data = await resp.json()

    return data

