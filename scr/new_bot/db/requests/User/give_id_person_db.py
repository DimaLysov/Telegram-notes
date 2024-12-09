from sqlalchemy import select

from new_bot.db.models import async_session, User


async def give_id_person(user_name: str) -> int | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_name == user_name))
        if not user:
            return None
        return user.id
