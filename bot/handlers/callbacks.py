from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from sqlalchemy.util import await_only

from bot.common import BallsCallbackFactory
from bot.db.models import PlayerScore, User, SapCategory
from bot.keyboard.keyboards import generate_balls

router = Router(name="callbacks-router")


@router.callback_query(BallsCallbackFactory.filter(F.color == "red"))
async def cb_miss(callback: CallbackQuery, session: AsyncSession):
    """
    Invoked on red ball tap
    :param callback: CallbackQuery from Telegram
    :param session: DB connection session
    """

    await session.merge(PlayerScore(user_id=callback.from_user.id, score=0))
    await session.commit()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text("Your score: 0", reply_markup=generate_balls())


@router.callback_query(BallsCallbackFactory.filter(F.color == "green"))
async def cb_hit(callback: CallbackQuery, session: AsyncSession):
    """
    Invoked on green ball tap
    :param callback:CallbackQuery from Telegram
    :param session: DB connection session
    """
    db_query = await session.execute(select(PlayerScore).filter_by(user_id=callback.from_user.id))
    player: PlayerScore = db_query.scalar()
    # Note: we're incrementing client-side, not server-side
    player.score += 1
    await session.commit()

    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f"Your score: {player.score}", reply_markup=generate_balls())


@router.callback_query(F.data.startswith('category_'))
async def sap_category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    from bot.keyboard.category import keyboard_sap_category
    message_text, reply_markup = await keyboard_sap_category(category_id)
    await callback.message.edit_text(text=message_text, reply_markup=reply_markup)


@router.callback_query(F.data.startswith('sap_category_'))
async def sap_category_item(callback: CallbackQuery):
    sap_category_id = int(callback.data.split('_')[2])
    from bot.keyboard.category import keyboard_sap_category_item
    message_text, reply_markup = await keyboard_sap_category_item(sap_category_id)
    await callback.message.delete()
    await callback.message.answer(text=message_text, reply_markup=reply_markup)


@router.callback_query(F.data.startswith('back_category'))
async def back_category(callback: CallbackQuery):
    from bot.keyboard.category import keyboard_category
    keyboard = await keyboard_category()
    await callback.message.edit_reply_markup(text="Maxsulotlar bo'limidan birini tanlang!", reply_markup=keyboard)


@router.callback_query(F.data.startswith('decrease_'))
async def decrease_quantity(callback: CallbackQuery):
    parts = callback.data.split('_')
    sap_category_id = int(parts[1])
    quantity = max(1, int(parts[2]) - 1)
    from bot.keyboard.category import keyboard_sap_category_item
    message_text, reply_markup = await keyboard_sap_category_item(sap_category_id, quantity)
    await callback.message.edit_text(message_text, reply_markup=reply_markup)
    await callback.answer()


@router.callback_query(F.data.startswith('increase_'))
async def increase_quantity(callback: CallbackQuery):
    parts = callback.data.split('_')
    sap_category_id = int(parts[1])
    quantity = max(1, int(parts[2]) + 1)
    from bot.keyboard.category import keyboard_sap_category_item
    message_text, reply_markup = await keyboard_sap_category_item(sap_category_id, quantity)
    await callback.message.edit_text(message_text, reply_markup=reply_markup)
    await callback.answer()


@router.callback_query(F.data.startswith('add_to_cart'))
async def add_to_cart(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = call.data.split('_')
    sap_category_id = int(data[3])
    new_quantity = int(data[4])
    user_id = call.from_user.id

    smtp = select(SapCategory).where(SapCategory.id ==sap_category_id)
    result = await session.execute(smtp)
    product = result.scalar_one_or_none()

    cart_data = await state.get_data()
    cart_items = cart_data.get("cart_items",[])
    found = False
    for item in cart_items:
        if item["id"] == sap_category_id:
            item["quantity"] += new_quantity
            found = True

    if not found:
        cart_items.append({
            "user_id": user_id,
            "id": sap_category_id,
            "name":product.name,
            "price":product.price,
            "quantity": new_quantity
        })

    await state.update_data(cart_items=cart_items)

    await call.answer(f"✅ {new_quantity} ta savatga qo‘shildi!")
