from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.types import ReplyKeyboardRemove

from new_bot.db.requests.Family.give_all_families_user import give_all_families_user
from new_bot.db.requests.User_Family.choose_family_db import choose_family_db
from new_bot.keyboards.all_keyboards import create_rat
from new_bot.utils.my_utils import Person

router_choose_family = Router()


class FormFamily(StatesGroup):
    chose_name_family = State()


@router_choose_family.message(Command('choice_family'))
async def process_name_family(m: Message, state: FSMContext):
    await state.set_state(FormFamily.chose_name_family)
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name,
                  surname=m.from_user.last_name)
    families = await give_all_families_user(user)
    if not families:
        await m.answer(text='У вас нет пока ни одной семьи\n'
                            'Чтобы создать семью введите команду /create_family')
        await state.clear()
    else:
        await m.answer(text='Введите название семьи, в которую хотите перейти', reply_markup=create_rat(families))


@router_choose_family.message(FormFamily.chose_name_family)
async def choose_family_hd(m: Message, state: FSMContext):
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name,
                  surname=m.from_user.last_name)
    answer = await choose_family_db(user, m.text)
    if answer == 1:
        await m.answer(text='Семьи с таким названием нет\n'
                            'Для того чтобы создать семью введите команду /create_family')
    elif answer == 2:
        await m.answer(text='Вы не можете перейти в данную семью, пока ее создатель вас не добавит в нее',
                       reply_markup=ReplyKeyboardRemove())
    elif answer == 3:
        await m.answer(text='Вы успешно перешли в семью', reply_markup=ReplyKeyboardRemove())
    await state.clear()
