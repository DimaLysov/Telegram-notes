from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from scr.config import BOT_API_TOKEN, ADMINS
from aiogram.fsm.storage.memory import MemoryStorage

# pg_db = PostgresHandler(config('PG_LINK'))
# scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in ADMINS.split(',')]
bot = Bot(token=BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=MemoryStorage())