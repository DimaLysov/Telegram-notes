from sqlalchemy import select

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.give_id_person_db import give_id_person


async def give_chosen_family_db(user: Person):
    user_id = await give_id_person(user.user_name)
    async with async_session() as session:
        user_family = session.scalar(
            select(UserFamily).where(UserFamily.user_id == user_id and UserFamily.status is True))
        return user_family.family_id
