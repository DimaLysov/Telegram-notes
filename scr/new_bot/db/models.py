from sqlalchemy import BigInteger, String, Boolean, ForeignKey, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from scr.config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    chat_id = Column(BigInteger, unique=True, default=None)
    name = Column(String)
    surname = Column(String)


class Family(Base):
    __tablename__ = 'families'

    id = Column(Integer, primary_key=True)
    name_family = Column(String, unique=True)


class UserFamily(Base):
    __tablename__ = 'users_families'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    family_id = Column(Integer, ForeignKey('families.id'))
    # Статус показывает выбрана семья или нет
    status = Column(Boolean, default=False)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    note = Column(String)
    user_family_id = Column(Integer, ForeignKey('users_families.id'))
    # Статус показывает выполнено ли событие
    status = Column(Boolean, default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
