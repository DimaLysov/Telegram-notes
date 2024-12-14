from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserFamily
from db.requests.User.give_id_person_db import give_id_person


async def give_id_link_user(user_name: str):
    user_id = await give_id_person(user_name)
    async with async_session() as session:
        user_family = await session.scalar(select(UserFamily).filter(and_(
            UserFamily.user_id == user_id,
            UserFamily.status.is_(True)
        )))
        if not user_family:
            return None
        return user_family.id
