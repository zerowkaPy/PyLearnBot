import os
import asyncpg
from asyncpg.connection import Connection
import asyncio
from dotenv import load_dotenv

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.user import User

load_dotenv(".venv")
DATABASE_URL = os.getenv("DATABASE_URL")


class SmartKeyboard:
    _instance = {}  # {user_id : instance}

    def __new__(cls, from_user: User):
        user_id = str(from_user.id)
        if user_id in cls._instance:
            return cls._instance[user_id]
        instance = super().__new__(cls)
        cls._instance[user_id] = instance
        return instance

    def __init__(self, user_id):
        if hasattr(self, "_initialized"): # защита от повторной инициализации
            return
        
        self.__user_id = str(user_id)
        self.__adjust = None
        self.__buttons = None
        self.__page_num = None
        self.__rest = None
        self.__rows_num = None
        self.__rows_num_cache = self.__rows_num
        self.__next_button = None
        self.__back_button = None
        self.__back_button_need = False
        self.__is_first_page = True
        self.__button_cache = []
        self.__page_counter = 0
        self.__page_cash = {} # {str(self.__page_counter) :self.__button_cache[0:]}
        self.__page_rollback = {}
        self._initialized = True  # флаг ініціалізації


    def __kb_prop(self):
        self.__page_num = len(self.__buttons) // self.__rows_num
        self.__rest = len(self.__buttons) % self.__rows_num
        if self.__page_num > 1:
            self.__set_back_button()

    def __prop_check(self):
        if self.__adjust:
            return True
        else:
            return False

    def set_prop(self, adjust:list[int], rows_num:int, next_button:str = "next", back_button:str = "back"):
        if not self.__buttons:
            raise SyntaxError("you must first execute 'add_buttons'")
        self.__adjust = adjust
        self.__rows_num = rows_num
        self.__next_button = next_button
        self.__back_button = back_button
        self.__kb_prop()
        self.__is_correct_adjust()

    def add_butons(self, buttons:list[str]):
        if type(buttons) != list:
            raise TypeError("buttons parameter must be a list of strings")
        if len(buttons) == 0:
            raise ValueError("buttons parameter must contain at least 1 string")
        self.__buttons = buttons

    def __add_page_in_cache(self):
        buttons = tuple(self.__button_cache[0:])
        self.__page_counter += 1
        counter = str(self.__page_counter)
        print("counter in add page cash", counter)
        self.__page_cash[counter] = buttons
        print(self.__page_cash[str(self.__page_counter)] )
        self.__button_cache.clear()

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
        
    def __set_back_button(self):
        self.__back_button_need = True
    def __remove_back_button(self):
        self.__back_button_need = False
    
    def __is_back_button_need(self):
        if self.__is_first_page:
            return False
        else:
            return True
        
    def __delete(self):
        self._instance.pop(self.__user_id)

    def __is_correct_adjust(self):
        summa = 0
        for adjust in self.__adjust:
            summa += adjust
        if summa > self.__rows_num:
            raise ValueError("adjusts summa mast be eqal to rows_num")
        
        
    def get_keyboard(self):
        if self.__prop_check():
            if self.__is_final():
                if self.__is_full():
                    builder = InlineKeyboardBuilder()
                    for button in range(self.__rows_num):
                        button_text = self.__buttons.pop(0)
                        self.__button_cache.append(button_text)
                        builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
                    self.__page_num -= 1
                    if self.__is_back_button_need():
                        builder.add(InlineKeyboardButton(text=self.__back_button, callback_data=self.__back_button))
                        self.__button_cache.append(self.__back_button)
                        builder.adjust(*self.__adjust, 1)
                    else:
                        builder.adjust(*self.__adjust)
                    # self.__delete()
                    self.__add_page_in_cache()
                    self.__is_first_page = False
                    return builder.as_markup()
                else:
                    builder = InlineKeyboardBuilder()
                    for button in range(self.__rest):
                        button_text = self.__buttons.pop(0)
                        self.__button_cache.append(button_text)
                        builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
                    self.__page_num -= 1
                    if self.__is_back_button_need():
                        builder.add(InlineKeyboardButton(text=self.__back_button, callback_data=self.__back_button))
                        self.__button_cache.append(self.__back_button)
                        builder.adjust(*self.__adjust, 1)
                    else:
                        builder.adjust(*self.__adjust)
                    # self.__delete()
                    self.__add_page_in_cache()
                    self.__is_first_page = False
                    return builder.as_markup()

            else:
                builder = InlineKeyboardBuilder()
                for button in range(self.__rows_num):
                    button_text = self.__buttons.pop(0)
                    self.__button_cache.append(button_text)
                    builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
                builder.add(InlineKeyboardButton(text=self.__next_button, callback_data=self.__next_button))
                self.__button_cache.append(self.__next_button)
                if self.__is_back_button_need():
                    builder.add(InlineKeyboardButton(text=self.__back_button, callback_data=self.__back_button))
                    self.__button_cache.append(self.__back_button)
                    builder.adjust(*self.__adjust, 1, 1)
                else:
                    builder.adjust(*self.__adjust, 1)
                self.__page_num -= 1
                self.__add_page_in_cache()
                self.__is_first_page = False
                return builder.as_markup()
            
                # if self.__is_correct_adjust():
                #     builder.adjust(*self.__adjust, 1)
                #     self.__page_num -= 1
                #     return builder.as_markup()
                # else:
                #     raise ValueError("adjusts summa mast be eqal to rows_num")
        else:
            raise RuntimeError("You must execute set_prop() before calling get_keyboard()")
        
    def previous_keyboard(self):
        self.__page_counter -= 1
        count = str(self.__page_counter)
        buttons = self.__page_cash[count]
        builder = InlineKeyboardBuilder()
        for button_text in buttons:
            builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
        builder.adjust(*self.__adjust, 1, 1)

        # Сначала >= x
        for key, value in self.__page_cash.items():
            if int(key) >= self.__page_counter + 1:
                self.__buttons.extend(value)
        # Потом < x
        for key, value in self.__page_cash.items():
            if int(key) < self.__page_counter + 1:
                self.__buttons.extend(value)

                self.__page_num +=1
                return builder.as_markup()



    