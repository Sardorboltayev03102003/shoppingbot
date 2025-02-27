from multiprocessing.resource_tracker import register

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.state import Register
from bot.keyboard.contact import contact_keyboard
from bot.request.add_user import add_user

router = Router(name="commands-router")


#
# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     """
#     Handles /start command
#     :param message: Telegram message with "/start" text
#     """
#     await message.answer(
#         "Hi there! This is a simple clicker bot. Tap on green ball, but don't tap on red ones!\n"
#         "If you tap a red ball, you'll have to start over.\n\n"
#         "Enough talk. Just tap /play and have fun!"
#     )
#
#
# @router.message(Command("play"))
# async def cmd_play(message: Message, session: AsyncSession):
#     """
#     Handles /play command
#     :param message: Telegram message with "/play" text
#     :param session: DB connection session
#     """
#     await session.merge(PlayerScore(user_id=message.from_user.id, score=0))
#     await session.commit()
#
#     await message.answer("Your score: 0", reply_markup=generate_balls())
#
#
# @router.message(Command("top"))
# async def cmd_top(message: Message, session: AsyncSession):
#     """
#     Handles /top command. Show top 5 players
#     :param message: Telegram message with "/top" text
#     :param session: DB connection session
#     """
#     sql = select(PlayerScore).order_by(PlayerScore.score.desc()).limit(5)
#     text_template = "Top 5 players:\n\n{scores}"
#     top_players_request = await session.execute(sql)
#     players = top_players_request.scalars()
#
#     score_entries = [f"{index+1}. ID{item.user_id}: {html.bold(item.score)}" for index, item in enumerate(players)]
#     score_entries_text = "\n".join(score_entries)\
#         .replace(f"{message.from_user.id}", f"{message.from_user.id} (it's you!)")
#     await message.answer(text_template.format(scores=score_entries_text), parse_mode="HTML")


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text="Ro'yxatdan o'tish uchun ismingizni kiriting:")
    await state.set_state(Register.fullname)


@router.message(Register.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer(text="Familiyangizni kiriting:")
    await state.set_state(Register.surname)


@router.message(Register.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer(text="Yoshingizni kiriting:")
    await state.set_state(Register.age)


@router.message(Register.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(text="Nomeringizni jo'nating:", reply_markup=contact_keyboard)
    await state.set_state(Register.number)


@router.message(Register.number)
async def process_number(message: Message, state: FSMContext, **kwargs):
    data = kwargs.get("data",{})
    session = data.get('session')
    print(data)
    if message.contact:
        number = message.contact.phone_number
    else:
        number = message.text
    user_data = await state.get_data()
    telegram_id = message.from_user.id
    fullname = user_data["fullname"]
    surname = user_data["surname"]
    age = user_data["age"]

    await add_user(telegram_id, fullname, surname, age, number,session)
    await message.answer("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
    await state.clear()
