import os
import asyncpg
from asyncpg.connection import Connection
import asyncio
from dotenv import load_dotenv

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

load_dotenv(".venv")
DATABASE_URL = os.getenv("DATABASE_URL")


class SmartKeyboard:
    _instance = {}  # {user_id : instance}

    def __new__(cls, user_id):
        user_id = str(user_id)
        if user_id in cls._instance:
            return cls._instance[user_id]
        instance = super().__new__(cls)
        cls._instance[user_id] = instance
        return instance

    def __init__(self, user_id):
        if hasattr(self, "_initialized"): # защита от повторной инициализации
            return
        
        self.__user_id = str(user_id)
        self.__conn = None
        self.__adjust = None
        self.__buttons = None
        self.__page_num = None
        self.__rest = None
        self.__rows_num = None
        self.__rows_num_cache = self.__rows_num
        self.__button_cache = []
        
        self._initialized = True  # флаг ініціалізації


    async def set_connect(self, db_url:str):
        conn = await asyncpg.connect(db_url)
        self.__conn = conn
        return self.__conn

    async def close_connect(self, conn:Connection):
        await conn.close()

    def __kb_prop(self):
        self.__page_num = len(self.__buttons) // self.__rows_num
        self.__rest = len(self.__buttons) % self.__rows_num
      

    def set_prop(self, adjust:list[int], rows_num:int):
        if not self.__buttons:
            raise SyntaxError("you must first execute 'add_buttons'")
        self.__adjust = adjust
        self.__rows_num = rows_num
        self.__kb_prop()

    def add_butons(self, buttons:list[str]):
        if type(buttons) != list:
            raise TypeError("buttons parameter must be a list of strings")
        if len(buttons) == 0:
            raise ValueError("buttons parameter must contain at least 1 string")
        self.__buttons = buttons

    def __is_final(self):
        if self.__page_num == 0:
            return True
        elif self.__page_num <= 1 and self.__rest == 0:
            return True
        else:
            return False

    def __is_full(self):
        if self.__page_num > 1:
            return True
        if self.__rest == 0:
            return True
        else:
            return False

    def __delete(self):
        self._instance.pop(self.__user_id)

    def __is_correct_adjust(self):
        summa = 0
        for adjust in self.__adjust:
            summa += adjust
        if summa > self.__rows_num:
            return False
        else:
            return True
        
        
    def get_keyboard(self):
        if self.__is_final():
            if self.__is_full():
                builder = InlineKeyboardBuilder()
                for button in range(self.__rows_num):
                    button_text = self.__buttons.pop(0)
                    self.__button_cache.append(button_text)
                    builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
                self.__page_num -= 1
                builder.adjust(*self.__adjust)
                self.__delete()
                return builder.as_markup()
            else:
                builder = InlineKeyboardBuilder()
                for button in range(self.__rest):
                    button_text = self.__buttons.pop(0)
                    self.__button_cache.append(button_text)
                    builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
                self.__page_num -= 1
                builder.adjust(*self.__adjust)
                self.__delete()
                return builder.as_markup()

        else: 
            builder = InlineKeyboardBuilder()
            for button in range(self.__rows_num):
                button_text = self.__buttons.pop(0)
                self.__button_cache.append(button_text)
                builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
            builder.add(InlineKeyboardButton(text='Далі ➡️', callback_data='next'))
            if self.__is_correct_adjust():
                builder.adjust(*self.__adjust, 1)
                self.__page_num -= 1
                return builder.as_markup()
            else:
                raise ValueError("adjusts summa mast be eqal to rows_num")

    