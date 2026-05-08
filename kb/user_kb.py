from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

__start = ReplyKeyboardBuilder()
__start.add(
    KeyboardButton(text="Задачі 🧩"),
    KeyboardButton(text="Гайд 📖")
)
start = __start.as_markup()

__ex_level = InlineKeyboardBuilder()
__ex_level.add(
    InlineKeyboardButton(text="Легкий", callback_data="easy")
)
ex_level = __ex_level.as_markup()