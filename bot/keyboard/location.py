from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_location = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗺 Mening manzillarim"), KeyboardButton(text="📍 Manzilni yuborish", request_location=True),],
        [KeyboardButton(text="Ortga qaytish 🔙 ")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

check_location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="HA"),KeyboardButton(text="YO'Q")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def address_kb(get_location):
    buttons = [[KeyboardButton(text=", ".join(item.address.rsplit(", ", 1)[:-1]))] for item in get_location]
    buttons.append([KeyboardButton(text="⬅️ Ortga",)])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

