from aiogram import Dispatcher, Bot
from config import BOT_API_TOKEN


async def main():
    dp = Dispatcher()
    bot = Bot(BOT_API_TOKEN)
