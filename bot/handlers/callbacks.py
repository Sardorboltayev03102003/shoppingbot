from contextlib import suppress

from aiogram import Router, F
from aiogram.client import bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputFile, FSInputFile, InputMediaPhoto
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from PIL import Image

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

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f"Your score: {player.score}", reply_markup=generate_balls())


@router.callback_query(F.data.startswith('category_'))
async def sap_category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    from bot.keyboard.category import keyboard_sap_category
    message_text, reply_markup, category_image = await keyboard_sap_category(category_id)
    image_path = f"{category_image}"
    try:
        with Image.open(image_path) as img:
            img = img.resize((400, 400))
            resized_image_path = "resized_image.png"
            img.save(resized_image_path)
        photo = FSInputFile(resized_image_path)
        await callback.message.delete()
        await callback.message.answer_photo(photo, caption=message_text, reply_markup=reply_markup)
    except FileNotFoundError:
        await callback.message.answer("❌ Kategoriya rasmi topilmadi!")


@router.callback_query(F.data.startswith('sap_category_'))
async def sap_category_item(callback: CallbackQuery):
    sap_category_id = int(callback.data.split('_')[2])
    from bot.keyboard.category import keyboard_sap_category_item
    message_text, reply_markup, sap_category_image = await keyboard_sap_category_item(sap_category_id)
    image_path = f"{sap_category_image}"
    resized_image_path = "resize_image.png"
    try:
        with Image.open(image_path) as img:
            img = img.resize((300, 300))
            img.save(resized_image_path)
        photo = FSInputFile(resized_image_path)
        await callback.message.delete()
        await callback.message.answer_photo(photo, caption=message_text, reply_markup=reply_markup)
    except FileNotFoundError:
        await callback.message.answer("Maxsulot rasmi topilmadi")


@router.callback_query(F.data.startswith('back_category'))
async def back_category(callback: CallbackQuery):
    from bot.keyboard.category import keyboard_category
    keyboard = await keyboard_category()
    await callback.message.delete()
    await callback.message.answer(text="Maxsulotlar bo'limidan birini tanlang!", reply_markup=keyboard)


@router.callback_query(F.data.startswith('decrease_'))
async def decrease_quantity(callback: CallbackQuery):
    parts = callback.data.split('_')
    sap_category_id = int(parts[1])
    quantity = max(1, int(parts[2]) - 1)
    from bot.keyboard.category import keyboard_sap_category_item
    _, reply_markup, _ = await keyboard_sap_category_item(sap_category_id, quantity)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
    await callback.answer()


@router.callback_query(F.data.startswith('increase_'))
async def increase_quantity(callback: CallbackQuery):
    parts = callback.data.split('_')
    sap_category_id = int(parts[1])
    quantity = max(1, int(parts[2]) + 1)
    from bot.keyboard.category import keyboard_sap_category_item
    _, reply_markup, _ = await keyboard_sap_category_item(sap_category_id, quantity)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
    await callback.answer()


@router.callback_query(F.data.startswith('add_to_cart'))
async def add_to_cart(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = call.data.split('_')
    sap_category_id = int(data[3])
    new_quantity = int(data[4])
    user_id = call.from_user.id

    smtp = select(SapCategory).where(SapCategory.id == sap_category_id)
    result = await session.execute(smtp)
    product = result.scalar_one_or_none()
    category_id = product.category_id

    cart_data = await state.get_data()
    cart_items = cart_data.get("cart_items", [])
    found = False
    for item in cart_items:
        if item["id"] == sap_category_id:
            item["quantity"] += new_quantity
            found = True

    if not found:
        cart_items.append({
            "user_id": user_id,
            "id": sap_category_id,
            "name": product.name,
            "price": product.price,
            "quantity": new_quantity
        })

    await state.update_data(cart_items=cart_items)
    await call.answer("Mahsulot savatga qo'shildi ✅")
    from bot.keyboard.category import keyboard_sap_category
    await call.message.delete()
    message_text, reply_markup,category_image = await keyboard_sap_category(category_id)
    photo = FSInputFile(category_image)
    await call.message.answer_photo(photo,caption=message_text,reply_markup=reply_markup)

@router.callback_query(F.data.startswith('clear_cart'))
async def clear_cart(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer("Savat tozalandi! 🛒❌")
