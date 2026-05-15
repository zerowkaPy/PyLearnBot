from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

_start = ReplyKeyboardBuilder()
_start.add(
    KeyboardButton(text="Задачі 🧩"),
    KeyboardButton(text="Гайд 📖")
)
start = _start.as_markup()

_ex_level = InlineKeyboardBuilder()
_ex_level.add(
    InlineKeyboardButton(text="Легкий", callback_data="easy"),
    InlineKeyboardButton(text="Середній", callback_data="middle"),
    InlineKeyboardButton(text="Важкий", callback_data="hard"),
    InlineKeyboardButton(text="На головну", callback_data="menu")
)
_ex_level.adjust(1,1,1,1)
ex_level = _ex_level.as_markup()

_menu = ReplyKeyboardBuilder()
_menu.add(KeyboardButton(text="На головну"))
menu = _menu.as_markup()