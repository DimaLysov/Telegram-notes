from sqlalchemy import select

from db.models import async_session
from db.models import Family
from db.requests.User_Family.give_chosen_family_db import give_chosen_family_db


async def give_family_user_db(user_name: str):
    family_id = await give_chosen_family_db(user_name)
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.id == family_id))
        if not family:
            return
        return family.name_family
