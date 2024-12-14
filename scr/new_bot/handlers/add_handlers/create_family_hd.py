from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from new_bot.db.requests.Family.create_family_db import create_family
from new_bot.utils.my_utils import Person

router_create_family = Router()


class FormFamily(StatesGroup):
    name_family = State()


@router_create_family.message(Command('create_family'))
async def new_family(message: Message, state: FSMContext):
    await state.set_state(FormFamily.name_family)
    await message.answer(text='Введите название для семьи, которую хотите создать')


@router_create_family.message(FormFamily.name_family)
async def add_new_family(m: Message, state: FSMContext):
    user_name = '@' + m.from_user.username
    answer = await create_family(user_name, m.text)
    if answer:
        await m.answer(text='Вы успешно создали семью')
    else:
        await m.answer(text='Семья с таким названием уже есть')
    await state.clear()
