from interfaces.bot.fsm import ChangeFSM
from services.user import UserService, User
from schemas.user import UserUpdate, UserProfile
from base.exceptions import AppError
from aiogram.fsm.context import FSMContext

async def process_change(
        change: str,
        user: User,
        state: FSMContext,
        user_service: UserService
) -> tuple[bool, str]:

    state = await state.get_state()

    process_params = {
        ChangeFSM.username: UserUpdate(username=change),
        ChangeFSM.name: UserUpdate(name=change),
        ChangeFSM.bio: UserUpdate(profile=UserProfile(bio=change)),
    }[state]

    try:
        await user_service.update_user(user, process_params)
        return True, "✅ Успешно обновлено!"
    except AppError as e:
        return (False, "❌ " + str(e))



