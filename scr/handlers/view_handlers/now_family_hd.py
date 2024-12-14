from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db.requests.Family.give_family_user_db import give_family_user_db

router_now_family = Router()


@router_now_family.message(Command('now_family'))
async def give_now_family(m: Message):
    user_name = '@' + m.from_user.username
    now_fml = await give_family_user_db(user_name)
    await m.answer(text=f'Выбрана семья - {now_fml}')
