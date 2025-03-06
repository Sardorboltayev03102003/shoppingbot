from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def cart_keyboard(all_sap_category):
    keyboard = InlineKeyboardBuilder()

    for item in  all_sap_category:
        sap_category_name = item['name']
        sap_category_price = item['price']
        quantity = item['quantity']
        btn_text = f"{sap_category_name} | {quantity} ta {sap_category_price} so'm "
        keyboard.add(InlineKeyboardButton(text=btn_text, callback_data="view_cart"))


    keyboard.row(
        InlineKeyboardButton(text="🗑 Savatni bo'shatish", callback_data="clear_cart"),
        InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="order_now")
    )
    keyboard.add(InlineKeyboardButton(text="Bosh sahifa", callback_data="to_main"))

    return keyboard.adjust(1).as_markup()