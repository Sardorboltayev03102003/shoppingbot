from bot.__main__ import session_maker
from sqlalchemy import select

from bot.db import Location


async def get_location(user_id:int):
    async with session_maker() as session:
        res = await session.execute(
            select(Location).where(Location.user_id==user_id)
        )
        location = res.scalars().all()
        return location
