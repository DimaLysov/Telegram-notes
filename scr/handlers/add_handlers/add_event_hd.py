from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.requests.Events.add_new_event_db import add_new_event_db

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
    answer = await add_new_event_db(user_name, user_adder, event)
    if answer:
        await m.answer(text='Вы успешно добавили событие')
    await state.clear()
