from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family, User
from new_bot.utils.my_utils import Person


async def add_new_user(new_user: Person):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_name == new_user.user_name))
        if not user:
            session.add(User(user_name=new_user.user_name,
                             name=new_user.name,
                             surname=new_user.surname))
            await session.commit()
            return True
        return False
