from sqlalchemy import select, update

from new_bot.db.models import async_session
from new_bot.db.models import Family
from new_bot.utils.my_utils import Person


async def add_new_event_db(user_name: str, adder_user_name: str, event: str):
    async with async_session() as session:
        pass
