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
