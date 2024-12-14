from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from new_bot.db.requests.Family.give_family_user_db import give_family_user_db
from new_bot.utils.my_utils import Person

router_now_family = Router()


@router_now_family.message(Command('now_family'))
async def give_now_family(m: Message):
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name.lower(),
                  surname=m.from_user.last_name)
    now_fml = await give_family_user_db(user)
    await m.answer(text=f'Выбрана семья - {now_fml}')
