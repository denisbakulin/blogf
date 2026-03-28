from auth.user_create import UserCreator
from base.db import session_maker
from utils.auth import generate_hashed_password
from services.admin import AdminService

async def create_admin_user(username: str, password: str):
    """Говно!!!"""
    try:
        async with session_maker() as session:
            logic = UserCreator(session)
            admin = AdminService(session)
            user = await logic.execute(username=username, name="admin")
            await logic.user_s.update_item(
                user.id, password=generate_hashed_password(password))

            await admin.create_admin(user_id=user.id)

    except:
        print("admin already exists")
