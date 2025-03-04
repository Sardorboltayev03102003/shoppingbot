from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


async def add_user(telegram_id: int, fullname: str, surname: str, age: int, number: str, session: AsyncSession):
    user = User(telegram_id=telegram_id, fullname=fullname, surname=surname, age=age, number=number)
    session.add(user)
    await session.commit()


async def get_user(telegram_id: int, session: AsyncSession):
    result = await session.execute(select(User).filter_by(telegram_id=telegram_id))
    return result.scalars().first()
