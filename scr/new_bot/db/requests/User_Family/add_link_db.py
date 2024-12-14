from sqlalchemy import select, and_

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.db.requests.Family.give_id_famiy_db import give_id_family
from new_bot.db.requests.User.give_id_person_db import give_id_person
from new_bot.db.requests.User_Family.update_status_db import update_status_db
from new_bot.utils.my_utils import Person


async def add_link(user_name: str, name_family: str):
    user_id = await give_id_person(user_name)
    family_id = await give_id_family(name_family)
    async with async_session() as session:
        link = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.family_id == family_id
        )))
        if not link:
            session.add(UserFamily(user_id=user_id, family_id=family_id))
            await session.commit()
        await update_status_db(user_name, name_family)
        return
