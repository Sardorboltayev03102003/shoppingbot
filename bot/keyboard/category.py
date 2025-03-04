from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.request.category import get_category, get_sap_category


async def keyboard_category():
    all_category = await get_category()
    keyboard = InlineKeyboardBuilder()
    if all_category:
        for cat in all_category:
            keyboard.add(
                InlineKeyboardButton(text=cat.name, callback_data=f"category_{cat.id}")

            )
    return keyboard.adjust(2).as_markup()
async def keyboard_sap_category(category_id):
    all_sap_category = await get_sap_category(category_id)
    keyboard = InlineKeyboardBuilder()
    all_sap_category = list(all_sap_category)
    if not all_sap_category:
        message_text = "Bu categoriyada maxsulot mavjud emas"
    else:
        message_text = "Maxsulotlar"
        for sap in all_sap_category:
            keyboard.add(
                InlineKeyboardButton(text=sap.name, callback_data=f"sap_category_{sap.id}")
            )
    keyboard.add(InlineKeyboardButton(text="Ortga",callback_data="back_to_category"))
    reply_markup = keyboard.adjust(2).as_markup()
    return message_text,reply_markup