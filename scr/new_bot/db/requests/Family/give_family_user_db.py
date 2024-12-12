from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family
from new_bot.db.requests.User_Family.give_chosen_family_db import give_chosen_family_db
from new_bot.utils.my_utils import Person


async def give_family_user_db(user: Person):
    family_id = await give_chosen_family_db(user)
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.id == family_id))
        if not family:
            return
        return family.name_family
