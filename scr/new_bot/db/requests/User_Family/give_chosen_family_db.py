from sqlalchemy import select, and_

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.give_id_person_db import give_id_person


async def give_chosen_family_db(user_name: str) -> int | None:
    user_id = await give_id_person(user_name)
    async with async_session() as session:
        family = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.status.is_(True)
        )))
        if not family:
            return None
        return family.family_id
