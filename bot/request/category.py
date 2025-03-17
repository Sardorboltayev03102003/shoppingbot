from sqlalchemy import select

from bot.__main__ import session_maker
from bot.db.models import *


async def get_category():
    async with session_maker() as session:
        return await session.scalars(select(Category))


async def get_sap_category(category_id: int):
    async with session_maker() as session:
        return await session.scalars(select(SapCategory).where(SapCategory.category_id == category_id))


async def get_category_details(category_id: int):
    async with session_maker() as session:
        res = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = res.scalar_one_or_none()
        return category


async def get_sap_category_item(sap_category_id: int):
    async with session_maker() as session:
        stmt = select(SapCategory).where(SapCategory.id == sap_category_id).limit(1)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()
