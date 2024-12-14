from sqlalchemy import select

from db.models import async_session
from db.models import Family
from db.requests.User_Family.add_link_db import add_link


async def create_family(user_name: str, name_family: str) -> bool:
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.name_family == name_family))
        if not family:
            session.add(Family(name_family=name_family))
            await session.commit()
            await add_link(user_name, name_family)
            return True
        return False
