from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


async def add_user(telegram_id:int,fullname:str,surname:str,age:int,number:str,session:AsyncSession):
    async with session.begin:
        user = User(telegram_id=telegram_id,fullname=fullname,surname=surname,age=age,number=number)
        session.add(user)

