from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from new_bot.db.requests.Family.give_family_user_db import give_family_user_db
from new_bot.db.requests.User.give_all_users_fml import give_all_users_fml
from new_bot.utils.my_utils import Person

router_all_pers_fml = Router()


@router_all_pers_fml.message(Command('view_family'))
async def give_all_pers_fml(m: Message):
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name.lower(),
                  surname=m.from_user.last_name)
    name_family = await give_family_user_db(user)
    users = await give_all_users_fml(name_family)
    print(users)
    answer = ''
    for number_user in range(len(users)):
        answer += f"{number_user + 1}) {users[number_user]['name'].capitalize()} {users[number_user]['surname'].capitalize()} ({users[number_user]['user_name']})\n"
    await m.answer(text=f'{answer}')
