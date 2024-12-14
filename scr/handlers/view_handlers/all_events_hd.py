from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.requests.Events.get_all_events_user_db import get_all_events_user_db

router_all_events = Router()


@router_all_events.message(Command('view_events'))
async def view_events(m: Message):
    user_name = '@' + m.from_user.username
    events = await get_all_events_user_db(user_name)
    print(events)
    answer = ''
    for num_event in range(len(events)):
        answer += f'{num_event+1}) {events[num_event]}\n'
    await m.answer(text=f'{answer}')
