from sqlalchemy import select

from db.models import async_session
from db.models import Event
from db.requests.User.give_id_person_db import give_id_person


async def get_all_events_user_db(user_name: str):
    user_id = await give_id_person(user_name)
    print(user_id)
    async with async_session() as session:
        events = await session.scalars(select(Event).filter(
            Event.user_id == user_id
        ))
        answer = [event.note for event in events]
        return answer
