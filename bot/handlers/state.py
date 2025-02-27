from aiogram.fsm.state import StatesGroup,State


class Register(StatesGroup):
    fullname = State()
    surname = State()
    age = State()
    number = State()