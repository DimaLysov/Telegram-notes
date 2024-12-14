from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from new_bot.db.requests.User_Family.give_chosen_family_db import give_chosen_family_db
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.add_new_user_db import add_new_user

router_add_event = Router()


class FormAddEvent(StatesGroup):
    tg_id = State()
    event = State()


@router_add_event.message(Command('add_event'))
async def accept_user(m: Message, state: FSMContext):
    await state.set_state(FormAddEvent.tg_id)
    await m.answer(text='Введите тег пользователя, для которого хотите добавить событие')


@router_add_event.message(FormAddEvent.tg_id)
async def accept_event(m: Message, state: FSMContext):
    await state.update_data(tg_id=m.text)
    await state.set_state(FormAddEvent.event)
    await m.answer(text='Напишите событие для человека')


@router_add_event.message(FormAddEvent.event)
async def add_event(m: Message, state: FSMContext):
    user_data = await state.get_data()
    user_name = user_data.get('tg_id')
    event = m.text
    user_adder = '@' + m.from_user.username

    await state.clear()
