from sqlalchemy import select

from db.models import async_session
from db.models import User
from db.requests.Family.give_family_user_db import give_family_user_db
from db.requests.User_Family.add_link_db import add_link
from utils.my_utils import Person


async def add_new_user(new_user: Person, adder_user_name: str):
    async with async_session() as session:
        answer = False
        user = await session.scalar(select(User).where(User.user_name == new_user.user_name))
        if not user:
            session.add(User(user_name=new_user.user_name,
                             name=new_user.name,
                             surname=new_user.surname))
            await session.commit()
            answer = True
        name_family = await give_family_user_db(adder_user_name)
        await add_link(new_user.user_name, name_family)
        return answer
