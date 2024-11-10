from aiogram import Dispatcher, Bot
from scr.config import BOT_API_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

