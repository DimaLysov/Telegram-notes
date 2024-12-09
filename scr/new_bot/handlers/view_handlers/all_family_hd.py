from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from new_bot.db.requests.Family.give_all_family_db import give_all_family

router_all_family = Router()


@router_all_family.message(Command('all_family'))
async def give_families(m: Message):
    all_families = await give_all_family()
    if all_families is None:
        await m.answer(text='Нет ни одной семьи')
        return
    answer = ''
    for family in all_families:
        answer += f'{family.name_family}\n'
    await m.answer(text=answer)
