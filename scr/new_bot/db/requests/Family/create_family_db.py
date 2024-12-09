from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User_Family.add_link_db import add_link


async def create_family(user: Person, name_family: str) -> bool:
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.name_family == name_family))
        if not family:
            session.add(Family(name_family=name_family))
            await session.commit()
            await add_link(user, name_family)
            return True
        return False
