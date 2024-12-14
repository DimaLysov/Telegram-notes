import asyncio

from sqlalchemy import select, and_

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily, User, Family
from new_bot.db.requests.User.give_id_person_db import give_id_person


async def give_all_families_user(user_name: str):
    user_id = await give_id_person(user_name)
    async with async_session() as session:
        families = await session.scalars(select(Family).join(UserFamily).filter(
            UserFamily.user_id == user_id
        ))
        answer = [family.name_family for family in families]
        return answer


