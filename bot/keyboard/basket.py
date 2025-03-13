from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def cart_keyboard(all_sap_category):
    keyboard = InlineKeyboardBuilder()

    for item in all_sap_category:
        sap_category_name = item['name']
        sap_category_price = item['price']
        quantity = item['quantity']
        btn_text = f"{sap_category_name} | {quantity} ta {sap_category_price} so'm "
        keyboard.add(InlineKeyboardButton(text=btn_text, callback_data="view_cart"))

    keyboard.row(
        InlineKeyboardButton(text="🗑 Savatni bo'shatish", callback_data="clear_cart"),
        InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="order_now")
    )

    # Birinchi mahsulotning `id` sini olish (agar mavjud bo'lsa)
    if all_sap_category:
        first_sap_category_id = all_sap_category[-1]['id']
        keyboard.add(InlineKeyboardButton(text="Ortga", callback_data=f"sap_category_{first_sap_category_id}"))

    return keyboard.adjust(1).as_markup()

