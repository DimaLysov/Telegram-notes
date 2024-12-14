from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router_help = Router()


@router_help.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(text='Список команд которые могут вам понадобиться:\n'
                              '/create_family - Создать семью\n'
                              '/choice_family - Сменить семью\n'
                              '/add_person - Добавить человека в семью\n'
                              '/add_event - Добавить событие для человека\n'
                              '/view_family - Показать состав семьи\n'
                              '/view_events - Показать события\n'
                              '/now_family - Показать выбранную семью\n')
