from db.models import async_session
from db.models import Event
from db.requests.User.give_id_person_db import give_id_person
from db.requests.User_Family.give_id_link_user_db import give_id_link_user


async def add_new_event_db(user_name: str, adder_user_name: str, event: str):
    id_user_family = await give_id_link_user(adder_user_name)
    user_id = await give_id_person(user_name)
    async with async_session() as session:
        session.add(Event(user_id=user_id, note=event, user_family_id=id_user_family))
        await session.commit()
        return True
