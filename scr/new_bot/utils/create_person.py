from aiogram.types import Message
from .my_utils import Person


def create_person(m: Message) -> Person:
    user = Person(user_name=m.from_user.username,
                  chat_id=m.from_user.id,
                  name=m.from_user.first_name,
                  surname=m.from_user.last_name)
    return user
