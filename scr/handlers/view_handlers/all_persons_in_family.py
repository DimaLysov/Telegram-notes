from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db.requests.Family.give_family_user_db import give_family_user_db
from db.requests.User.give_all_users_fml_db import give_all_users_fml_db

router_all_pers_fml = Router()


@router_all_pers_fml.message(Command('view_family'))
async def give_all_pers_fml(m: Message):
    user_name = '@' + m.from_user.username
    name_family = await give_family_user_db(user_name)
    users = await give_all_users_fml_db(name_family)
    print(users)
    answer = ''
    for number_user in range(len(users)):
        answer += f"{number_user + 1}) {users[number_user]['name'].capitalize()} {users[number_user]['surname'].capitalize()} ({users[number_user]['user_name']})\n"
    await m.answer(text=f'{answer}')
