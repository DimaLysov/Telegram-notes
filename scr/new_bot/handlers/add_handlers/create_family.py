from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from new_bot.db.requests.Family.create_family import create_family

router_create_family = Router()


class FormFamily(StatesGroup):
    name_family = State()


@router_create_family.message(Command('create_family'))
async def new_family(message: Message, state: FSMContext):
    await state.set_state(FormFamily.name_family)
    await message.answer(text='Введите название для семьи, которую хотите создать')


@router_create_family.message(FormFamily.name_family)
async def add_new_family(message: Message, state: FSMContext):
    answer = await create_family(message.text)
    if answer:
        await message.answer(text='Вы успешно создали семью')
    else:
        await message.answer(text='Семья с таким названием уже есть')
    await state.clear()
