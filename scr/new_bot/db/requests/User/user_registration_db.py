from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import User
from new_bot.utils.my_utils import Person


async def user_registration(new_user: Person):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_name == new_user.user_name))
        if not user:
            session.add(User(**new_user.__dict__))
            await session.commit()
            return False
        elif user.chat_id is None:
            user.chat_id = new_user.chat_id
            user.name = new_user.name
            user.surname = new_user.surname
            await session.commit()
            return True
