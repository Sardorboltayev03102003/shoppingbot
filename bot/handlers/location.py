from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from geopy import Nominatim
from sqlalchemy.ext.asyncio import AsyncSession

import re

from bot.db import Location
from bot.keyboard import keyboard_location
from bot.keyboard import check_location_kb
from bot.keyboard.keyboards import main
from bot.keyboard.location import address_kb
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


@router.message(F.text.in_(["🗺 Mening manzillarim","⬅️ Ortga"]))
async def address_name(message: Message, session: AsyncSession):
    if message.text=="🗺 Mening manzillarim":
        telegram_id = message.from_user.id
        user_id = await get_user_id(telegram_id, session)
        from bot.request.location import get_location
        address = await get_location(user_id)
        address_btn = await address_kb(address)
        await message.answer(text="quyidagi manzillaringizdan birini tanlang",reply_markup=address_btn)
    elif message.text=="⬅️ Ortga":
        await message.answer(text="quyidagilardan birini tanlang",reply_markup=keyboard_location)





@router.message(F.text.in_(["HA", "YO'Q", "Ortga qaytish 🔙"]))
async def check_location(message: Message, session: AsyncSession,state:FSMContext):
    telegram_id = message.from_user.id
    user_id = await get_user_id(telegram_id, session)

    if message.text == "HA":
        if user_id in location_data:
            latitude = location_data[user_id]["latitude"]
            longitude = location_data[user_id]["longitude"]
            address = location_data[user_id]["address"]

            address = re.sub(r'^[^,]+,', '', address).strip()
            clean_address = re.sub(r'\b(Tumani|t\.|Shahar|sh\.|Ko‘cha|k\.|Oʻzbekiston|Uzbekistan|Davlat)\b', '',
                                   address, flags=re.IGNORECASE).strip()

            new_location = Location(user_id=user_id, latitude=latitude, longitude=longitude, address=clean_address)
            session.add(new_location)
            await session.commit()
            await session.close()



            await session.refresh(new_location)
            location_id = new_location.id

            await state.update_data(location_id=location_id)

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

@router.message(F.text == "/state_info")
async def show_state_data(message: Message, state: FSMContext):
    data = await state.get_data()  # State dagi barcha ma'lumotlarni olish
    if not data:
        await message.answer("ℹ️ State ichida ma'lumot yo'q.")
    else:
        info = "\n".join([f"{key}: {value}" for key, value in data.items()])
        await message.answer(f"📋 State dagi ma'lumotlar:\n\n{info}")
