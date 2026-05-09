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