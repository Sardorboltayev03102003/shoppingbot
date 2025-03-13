
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.request.category import get_category, get_sap_category, get_sap_category_item, get_category_details


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
    category = await get_category_details(category_id)
    keyboard = InlineKeyboardBuilder()
    all_sap_category = list(all_sap_category)

    category_image = category.image if category else None

    if not all_sap_category:
        message_text = "Bu categoriyada maxsulot mavjud emas"
    else:
        message_text = "Maxsulotlar"
        for sap in all_sap_category:
            keyboard.add(
                InlineKeyboardButton(text=sap.name, callback_data=f"sap_category_{sap.id}")
            )
    keyboard.row(InlineKeyboardButton(text="Ortga", callback_data="back_category"))
    reply_markup = keyboard.adjust(2).as_markup()
    return message_text, reply_markup, category_image


async def keyboard_sap_category_item(sap_category_id: int, quantity: int = 1):
    sap_category = await get_sap_category_item(sap_category_id)
    sap_category_image = sap_category.image if sap_category else None
    keyboard = InlineKeyboardBuilder()
    message_text = (
        f"🛍 <b>{sap_category.name}</b>\n"
        f"📜 <i>{sap_category.title}</i>\n"
        f"💰 Narxi: {sap_category.price} so‘m"
    )
    keyboard.row(
        InlineKeyboardButton(text="➖", callback_data=f"decrease_{sap_category.id}_{quantity}"),
        InlineKeyboardButton(text=f"{quantity}", callback_data=f"quantity"),
        InlineKeyboardButton(text="➕", callback_data=f"increase_{sap_category.id}_{quantity}")
    )
    keyboard.row(
        InlineKeyboardButton(text="Savatga qo'shish",callback_data=f"add_to_cart_{sap_category_id}_{quantity}")
    )
    keyboard.add(
        InlineKeyboardButton(text="Ortga",callback_data=f"category_{sap_category.category_id}")
    )

    reply_markup = keyboard.as_markup()
    return message_text,reply_markup,sap_category_image
