from sqlalchemy import select

from db.models import async_session
from db.models import Family


async def give_all_family():
    async with async_session() as session:
        family = await session.scalar(select(Family))
        if not family:
            return None
        return await session.scalars(select(Family))
