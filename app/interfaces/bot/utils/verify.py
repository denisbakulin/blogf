from auth.telegram import  AsyncSession, TelegramAuth


async def verify_user(
        session: AsyncSession,
        code: str, tg_id: int
) -> tuple[bool, str]:

    auth = TelegramAuth(session)

    result = await auth.verify(code=code, tg_id=tg_id)

    success = result.get("status", False)
    msg = result.get("msg", "default")

    return (success, msg)

