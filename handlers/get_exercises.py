from aiogram import Bot, Dispatcher, Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.types import MenuButton, MenuButtonCommands, BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from routers import user_router
from kb import user_kb
from kb.smart_keyboard import SmartKeyboard

@user_router.message(F.text == "Задачі 🧩")
async def exercises(message:Message):
    await message.answer("Оберіть рівень складності", reply_markup=user_kb.ex_level)

@user_router.callback_query(F.data == "easy")
async def kb_try(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    kb.init_keyboard()
    kb.add_butons(["Задача 1: print()"])
    kb.set_prop([6], 1, back_button="Назад", next_button="Далі")
    await callback.message.edit_text("Треба ще більше кнопок...", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "middle")
async def kb_try1(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    kb.init_keyboard()
    kb.add_butons(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '35' ])
    kb.set_prop([3,2], 5, back_button="Назад", next_button="Далі", home_button="На головну")
    await callback.message.edit_text("Треба ще більше кнопок...", reply_markup=kb.get_keyboard())


@user_router.callback_query(F.data == "На головну")
async def kb_try2(callback:CallbackQuery):
    SmartKeyboard.delete_user(callback.from_user)
    await callback.message.answer(
"""Ви повернулися на головну""",
reply_markup=user_kb.start
)
    await callback.message.delete()


@user_router.callback_query(F.data == "Далі")
async def next(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    await callback.message.edit_text(text="ви перейшли на наступну сторінку клавіатури", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "Назад")
async def next(callback:CallbackQuery):
    kb = SmartKeyboard(callback.from_user)
    await callback.message.edit_text(text="ви перейшли на минулу сторінку клавіатури", reply_markup=kb.previous_keyboard())