from usecases.auth import AuthLogic, AsyncSession


async def verify_user(
        session: AsyncSession,
        code: str, tg_id: int
) -> tuple[bool, str]:

    auth = AuthLogic(session)

    result = await auth.verify_with_telegram(code=code, tg_id=tg_id)

    success = result.get("status", False)
    msg = result.get("msg", "default")

    return (success, msg)

