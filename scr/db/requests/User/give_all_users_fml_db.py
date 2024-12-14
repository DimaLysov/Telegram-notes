from sqlalchemy import select

from db.models import async_session
from db.models import User, UserFamily
from db.requests.Family.give_id_famiy_db import give_id_family


async def give_all_users_fml_db(name_family):
    family_id = await give_id_family(name_family)
    async with async_session() as session:
        users = await session.scalars(select(User).join(UserFamily).filter(
            UserFamily.family_id == family_id
        ))
        answer = []
        for user in users:
            data_user = {'user_name': user.user_name}
            if user.name is None:
                data_user['name'] = ''
            else:
                data_user['name'] = user.name
            if user.surname is None:
                data_user['surname'] = ''
            else:
                data_user['surname'] = user.surname
            answer.append(data_user)
        return answer
