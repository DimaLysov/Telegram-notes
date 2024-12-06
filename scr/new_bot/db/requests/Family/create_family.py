from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family, User
from new_bot.utils.my_utils import Person


async def create_family(name_family: str) -> bool:
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.name_family == name_family))
        if not family:
            session.add(Family(name_family=name_family))
            await session.commit()
            return True
        return False
