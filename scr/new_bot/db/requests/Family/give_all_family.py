from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family, User
from new_bot.utils.my_utils import Person


async def give_all_family():
    async with async_session() as session:
        family = await session.scalar(select(Family))
        if not family:
            return None
        return await session.scalars(select(Family))
