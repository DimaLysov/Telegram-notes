from sqlalchemy import select

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.db.requests.Family.give_id_famiy_db import give_id_family
from new_bot.db.requests.User.give_id_person_db import give_id_person
from new_bot.utils.my_utils import Person


async def choose_family_db(user: Person, name_family: str):
    user_id = await give_id_person(user.user_name)
    family_id = await give_id_family(name_family)
    async with async_session() as session:
        user_family = await session.scalar(
            select(UserFamily).where(UserFamily.user_id == user_id and UserFamily.family_id == family_id))
        if not user_family:
            return False
        else:
            user_family.status = True
            await session.commit()
            return True
