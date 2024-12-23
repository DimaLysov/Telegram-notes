from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserFamily, Family
from db.requests.Family.give_id_famiy_db import give_id_family
from db.requests.User.give_id_person_db import give_id_person
from db.requests.User_Family.update_status_db import update_status_db


async def choose_family_db(user_name: str, name_new_family: str):
    user_id = await give_id_person(user_name)
    family_id = await give_id_family(name_new_family)
    async with async_session() as session:
        family = await session.scalar(select(Family).where(Family.name_family == name_new_family))
        if not family:
            return 1
        user_family = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.family_id == family_id
        )))
        if not user_family:
            return 2
        else:
            await update_status_db(user_name, name_new_family)
            return 3
