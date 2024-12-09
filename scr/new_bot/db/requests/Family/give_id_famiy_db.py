from sqlalchemy import select

from new_bot.db.models import async_session
from new_bot.db.models import Family


async def give_id_family(name_family: str) -> int | None:
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.name_family == name_family))
        if not family:
            return None
        return family.id
