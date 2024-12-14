from sqlalchemy import select, and_

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.db.requests.User.give_id_person_db import give_id_person
from new_bot.utils.my_utils import Person
from new_bot.db.requests.Family.give_id_famiy_db import give_id_family


async def update_status_db(user_name: str, name_new_family):
    user_id = await give_id_person(user_name)
    async with async_session() as session:
        old_user_family = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.status.is_(True)
        )))
        if old_user_family:
            print(1, '-', old_user_family.user_id, old_user_family.family_id, old_user_family.status)
            old_user_family.status = False
            print(2, '-', old_user_family.user_id, old_user_family.family_id, old_user_family.status)
        new_family_id = await give_id_family(name_new_family)
        print(f'new_family_id: {new_family_id}')
        new_user_family = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.family_id == new_family_id
        )))
        new_user_family.status = True
        print(3, '-', new_user_family.user_id, new_user_family.family_id, new_user_family.status)
        await session.commit()
        print()
        return
