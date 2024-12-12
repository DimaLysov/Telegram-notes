from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from new_bot.db.requests.User_Family.give_chosen_family_db import give_chosen_family_db
from new_bot.utils.my_utils import Person
from new_bot.db.requests.User.add_new_user_db import add_new_user

router_add_person = Router()


class FormUser(StatesGroup):
    tg_name = State()


@router_add_person.message(Command('add_person'))
async def add_new_persona(m: Message, state: FSMContext):
    await state.set_state(FormUser.tg_name)
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name,
                  surname=m.from_user.last_name)
    answer = await give_chosen_family_db(user)
    if answer is None:
        await m.answer(text='Вы не можете добавит человека, пока не выберите семью\n'
                            'Чтобы выбрать семью, выведите команду /choice_family')
        await state.clear()
    else:
        await m.answer(text='Введите телеграмм тег человека')


@router_add_person.message(FormUser.tg_name)
async def add_person(m: Message, state: FSMContext):
    await state.update_data(tg_name=m.text)
    user_data = await state.get_data()
    user_name = user_data.get('tg_name')
    new_user = Person(user_name=user_name,
                      chat_id=None,
                      name=' ',
                      surname=' ')
    adder_user = Person(user_name=m.from_user.username,
                        chat_id=m.from_user.id,
                        name=m.from_user.first_name,
                        surname=m.from_user.last_name)
    answer = await add_new_user(new_user, adder_user)
    if answer:
        await m.answer(text='Вы успешно зарегистрировали человека и добавили в семью')
    else:
        await m.answer(text='Вы успешно добавили человека в семью')
    await state.clear()
