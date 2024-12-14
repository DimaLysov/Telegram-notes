from sqlalchemy import select, and_

from new_bot.db.models import async_session
from new_bot.db.models import UserFamily
from new_bot.db.requests.User_Family.give_chosen_family_db import give_chosen_family_db
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.give_id_person_db import give_id_person


async def give_id_link_user(user_name: str):
    name_family = await give_chosen_family_db()
