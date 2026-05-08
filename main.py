import asyncio
import aiogram
import asyncpg


import sys
import logging
import subprocess
import tempfile
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.types import MenuButton, MenuButtonCommands, BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from kb.smart_keyboard import SmartKeyboard

load_dotenv("params.venv")
BOT_TOKEN = getenv("BOT_TOKEN")
import filters  

from handlers import guide, get_exercises
from routers import user_router, admin_router
from kb import user_kb


dp = Dispatcher()
dp.include_routers(user_router, admin_router)
user_router.message.filter(filters.UserFilter())
admin_router.message.filter(filters.AdminFilter())


@user_router.message(CommandStart())
async def start_user_handler(message:Message):
    await message.answer(
"""Ласкаво просимо!

Цей бот присвячений нашій улюбленій мові програмування

Не гайте часу, ознайомтеся з правилами користуванням бота (це дуже важливо) натиснувши кнопку"""\
""" "Гайд" або /guide та почніть проходити вправи 🏆 """,

reply_markup=user_kb.start
)


@admin_router.message(CommandStart())
async def start_admin_handler(message:Message):
    pass

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="запустити бота")
    ])
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
