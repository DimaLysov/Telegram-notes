from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from new_bot.db.requests.User.user_registration_db import user_registration
from new_bot.utils.my_utils import Person

router_start = Router()


@router_start.message(Command('start'))
async def cmd_start(m: Message):
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name.lower(),
                  surname=m.from_user.last_name)
    print(user.user_name)
    await user_registration(user)
    await m.answer(f'Добро пожаловать\n'
                   f'Создайте новую семью или войдите в уже существующую')

# @start_router.message(Command('start_2'))
# async def cmd_start_2(message: Message):
#     await message.answer('специальные кнопки', reply_markup=create_spec_kb())
#
#
# @start_router.message(Command('start_3'))
# async def cmd_start_3(message: Message):
#     await message.answer('builder кнопок', reply_markup=create_rat())
#
#
# @start_router.message(F.text == 'Давай инлайн!')
# async def get_inline_btn_link(message: Message):
#     await message.answer('Клавиатура с ссылками', reply_markup=easy_link_kb())
