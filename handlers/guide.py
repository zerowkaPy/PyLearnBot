from aiogram.types import Message
from aiogram import F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from routers import user_router

@user_router.message(F.text == "Гайд 📖")
@user_router.message(Command("guide"))
async def guide(message:Message):
    await message.answer(
"""Ми пропонуємо вам невеликі але дуже корисні завдання для покращення або пітримання ваших навичок з  Python

Задачі бувають трьох типів:
    ✏️ Задачі на написання коду
    💻 Задачі на передбачення результату виконання коду
    🗨️ Задачі з вибором правильної відповіді
    
Задачі на написання коду:

Вам буде дано опис завдання.
Ви повинні написати код і відправити його ботові.
Ви можете відправляти код звичайним текстом, наприклад:

def hello(text):
    print(text)
hello("Hello, World!")

але рекомендується відправляти код за допомогою вбудованого в Telegram "Блока коду":

\\`\\`\\`python
def hello(text):
    print(text)
hello("Hello, World!")
\\`\\`\\`

Таке повідомлення в телеграм буде відображатися прямісінько ось так:
```python
def hello(text):
    print(text)
hello("Hello, World!")
```
Ключеве слово "python" після \\`\\`\\` потрібно лише для підсвітки синтаксису Python. Цим словом можна знехтувати, якщо вам це не потрібно
""",
parse_mode=ParseMode.MARKDOWN
    )