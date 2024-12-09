from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.add_new_user_db import add_new_user

router_add_person = Router()


class FormUser(StatesGroup):
    name_user = State()
    tg_name = State()


@router_add_person.message(Command('add_person'))
async def add_new_persona(m: Message, state: FSMContext):
    await state.set_state(FormUser.name_user)
    await m.answer(text='Введите имя и фамилия человека')


@router_add_person.message(FormUser.name_user)
async def process_tg_name(m: Message, state: FSMContext):
    await state.update_data(name_user=m.text)
    await state.set_state(FormUser.tg_name)
    await m.answer(text='Введите телеграмм тег человека')


@router_add_person.message(FormUser.tg_name)
async def add_person(m: Message, state: FSMContext):
    await state.update_data(tg_name=m.text)
    user_data = await state.get_data()
    name, surname = user_data.get('name_user').split()
    user_name = user_data.get('tg_name')
    user = Person(user_name=user_name,
                  chat_id=None,
                  name=name,
                  surname=surname)
    answer = await add_new_user(user)
    if answer:
        await m.answer(text='Вы успешно добавили человека')
    else:
        await m.answer(text='Такой человек уже есть')
    await state.clear()
