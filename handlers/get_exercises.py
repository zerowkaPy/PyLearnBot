from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message, CallbackQuery

from exercises import easy
from routers import user_router, user_tasks
from kb import user_kb
from kb.smart_keyboard import SmartKeyboard

user_router.include_router(user_tasks)

@user_router.message(F.text == "Задачі 🧩")
async def exercises(message:Message):
    await message.answer("Оберіть рівень складності", reply_markup=user_kb.ex_level)

@user_router.callback_query(F.data == "easy")
async def easy_ex(callback:CallbackQuery, state:FSMContext):
    kb = SmartKeyboard(callback.from_user)
    kb.init_keyboard()
    kb.add_butons([
        "Задача 1: print()",
        "Задача 2: split()"
        ])
    kb.set_prop([1], 2, back_button="⬅️", next_button="➡️", home_button="Назад")
    await state.set_state("tasks")
    await callback.message.edit_text("Виберіть задачу", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "middle")
async def middle_ex(callback:CallbackQuery, state:FSMContext):
    await state.set_state("tasks")


@user_router.callback_query(F.data == "Назад")
async def change_diff(callbcack:CallbackQuery):
    await callbcack.message.answer("Оберіть рівень складності", reply_markup=user_kb.ex_level)
    await callbcack.message.delete()

@user_router.callback_query(F.data == "menu")
async def menu(callback:CallbackQuery, state:FSMContext):
    if SmartKeyboard.check_user(callback.from_user):
        SmartKeyboard.delete_user(callback.from_user)
    await callback.message.answer(
"""Ви повернулися на головну""",
reply_markup=user_kb.start)
    await callback.message.delete()
    await state.clear()

@user_router.callback_query(F.data == "➡️")
async def next(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    await callback.message.edit_text(text="ви перейшли на наступну сторінку клавіатури", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "⬅️")
async def previous(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    await callback.message.edit_text(text="ви перейшли на минулу сторінку клавіатури", reply_markup=kb.previous_keyboard())
