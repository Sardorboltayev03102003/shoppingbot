from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from geopy import Nominatim
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import Location
from bot.keyboard import keyboard_location
from bot.keyboard import check_location_kb
from bot.keyboard.keyboards import main
from bot.request.user import get_user_id

router = Router(name="callbacks-router")


@router.callback_query(F.data.startswith("order_now"))
async def location_list(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(text="Buyurtma berish uchun quyidagilardan birini tanlang!! ",
                              reply_markup=keyboard_location)


geolocator = Nominatim(user_agent="marketbot")

location_data = {}


@router.message(F.location)
async def location_receives(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    user_id = await get_user_id(telegram_id, session)
    latitude = message.location.latitude
    longitude = message.location.longitude

    location = geolocator.reverse((latitude, longitude), language="uz")
    address = location.address if location else None

    location_data[user_id] = {
        "latitude": latitude,
        "longitude": longitude,
        "address": address
    }
    await message.answer(text=f"📍 Joylashuvingiz saqlandi!\n\n"
                              f"🌍 <b>Kenglik:</b> {latitude}\n"
                              f"🌍 <b>Uzunlik:</b> {longitude}\n"
                              f"🏠 <b>Manzil:</b> {address}",
                         parse_mode="HTML", reply_markup=check_location_kb)


@router.message(F.text.in_(["HA", "YO'Q", "Ortga qaytish 🔙"]))
async def check_location(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    user_id = await get_user_id(telegram_id, session)

    if message.text == "HA":
        if user_id in location_data:
            latitude = location_data[user_id]["latitude"]
            longitude = location_data[user_id]["longitude"]
            address = location_data[user_id]["address"]

            new_location = Location(user_id=user_id, latitude=latitude, longitude=longitude, address=address)
            session.add(new_location)
            await session.commit()
            await session.close()

            del location_data[user_id]
            print("saqlandi")
        else:
            print("saqlanmadi")
    elif message.text == "YO'Q":
        await message.delete()
        await message.answer(text="Buyurtma berish uchun quyidagilardan birini tanlang!! ",
                             reply_markup=keyboard_location)

    elif message.text.strip() == "Ortga qaytish 🔙":
        await message.answer(text="bo'limlardan birini tanlang", reply_markup=main)
