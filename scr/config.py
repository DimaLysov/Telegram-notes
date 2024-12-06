import os

from dotenv import load_dotenv

load_dotenv()
# для базы данных
DB = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv('POSTGRES_HOST')
PORT = os.getenv('POSTGRES_PORT')

# SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
DATABASE_URL_SYNC = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

# для телеграмм
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ADMINS = os.getenv('ADMINS')

# BOT_CONTEXT_DEPTH = int(os.getenv('BOT_CONTEXT_DEPTH', default=10))
