from random import randint

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from bot.common import BallsCallbackFactory


def generate_balls() -> InlineKeyboardMarkup:
    """
    Generates a new 3x3 play field with 8 red balls and 1 green ball
    :return: Inline keyboard
    """
    balls_mask = [False] * 9
    balls_mask[randint(0, 8)] = True
    balls = ["🔴", "🟢"]
    data = ["red", "green"]
    builder = InlineKeyboardBuilder()
    for item in balls_mask:
        builder.button(
            text=balls[item],
            callback_data=BallsCallbackFactory(color=data[item]).pack()
        )
    return builder.adjust(3).as_markup()

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Maxsulotlar")],
        [KeyboardButton(text="Sozlamalar"), KeyboardButton(text="Savatcha")],
        [KeyboardButton(text="Yordam")],
    ],
    resize_keyboard=True
)

