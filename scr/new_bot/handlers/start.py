from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from new_bot.keyboards.all_keyboards import main_kb, create_spec_kb, create_rat

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(f'Привет')
    await message.answer('Вот кнопки', reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer('специальные кнопки', reply_markup=create_spec_kb())


@start_router.message(Command('start_3'))
async def cmd_start_3(message: Message):
    await message.answer('builder кнопок', reply_markup=create_rat())