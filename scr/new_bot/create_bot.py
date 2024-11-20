from aiogram import Dispatcher, Bot
from scr.config import BOT_API_TOKEN, ADMIN
from aiogram.fsm.storage.memory import MemoryStorage

# pg_db = PostgresHandler(config('PG_LINK'))
# scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in ADMIN.split(',')]
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())